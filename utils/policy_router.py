"""
Policy Router - Routes queries to appropriate verification tier

Uses JSON policy classification to determine:
- PROCEDURAL policies → Tier 1 (pattern/LLM check, no OCaml)
- PRIMARY policies → Tier 2 (OCaml formal verification)

This integrates:
- policies/procedural_policies.json (natural language)
- policies/primary_policies.json (natural language)
- policies/HIPAA_PRIMARY.policy (FOTL for OCaml)
- policies/HIPAA_PROCEDURAL.policy (FOTL for OCaml)
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class PolicyRouter:
    """
    Routes queries to appropriate policy tier based on JSON classification
    
    Uses JSON files to determine if query is about:
    - PROCEDURAL rules (how-to-comply) → Tier 1
    - PRIMARY rules (substantive permissions/prohibitions) → Tier 2
    """
    
    def __init__(self, 
                 procedural_json: str = "policies/procedural_policies.json",
                 primary_json: str = "policies/primary_policies.json"):
        
        self.procedural_json = Path(procedural_json)
        self.primary_json = Path(primary_json)
        
        # Load JSON files
        self.procedural_policies = self._load_json(self.procedural_json)
        self.primary_policies = self._load_json(self.primary_json)
        
        # Build keyword indices for fast lookup
        self.procedural_keywords = self._build_keyword_index(self.procedural_policies)
        self.primary_keywords = self._build_keyword_index(self.primary_policies)
        
        print(f"📚 Policy Router initialized:")
        print(f"   - {len(self.procedural_policies)} procedural policies")
        print(f"   - {len(self.primary_policies)} primary policies")
    
    def _load_json(self, path: Path) -> List[Dict]:
        """Load JSON policy file"""
        if not path.exists():
            print(f"⚠️ Warning: {path} not found, using empty policy list")
            return []
        
        try:
            with open(path) as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'policies' in data:
                    return data['policies']
                else:
                    print(f"⚠️ Warning: Unexpected JSON format in {path}")
                    return []
        except Exception as e:
            print(f"❌ Error loading {path}: {e}")
            return []
    
    def _build_keyword_index(self, policies: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Build keyword index for fast lookup
        
        Returns:
            {word: [policies containing that word]}
        """
        index = {}
        
        for policy in policies:
            # Extract text from various possible fields
            text = policy.get('text', '')
            if not text:
                text = policy.get('description', '')
            if not text:
                text = policy.get('natural_language', '')
            
            text_lower = text.lower()
            words = text_lower.split()
            
            # Index by meaningful words (>3 chars)
            for word in words:
                word_clean = word.strip('.,;:!?()[]{}')
                if len(word_clean) > 3:
                    if word_clean not in index:
                        index[word_clean] = []
                    if policy not in index[word_clean]:
                        index[word_clean].append(policy)
        
        return index
    
    def route_query(self, query: str, facts: List[List] = None) -> Tuple[str, List[Dict]]:
        """
        Route query to appropriate tier
        
        Args:
            query: Natural language query
            facts: Optional extracted facts (for additional context)
            
        Returns:
            (tier, relevant_policies)
            tier: "procedural" or "primary"
            relevant_policies: List of relevant policy dicts
        """
        
        query_lower = query.lower()
        
        # Step 1: Score against both policy types
        procedural_score = self._score_against_policies(
            query_lower, 
            self.procedural_policies,
            self.procedural_keywords
        )
        
        primary_score = self._score_against_policies(
            query_lower,
            self.primary_policies,
            self.primary_keywords
        )
        
        # Step 2: Detect procedural indicators in query
        procedural_indicators = [
            'professional judgment',
            'may use',
            'may disclose',
            'is permitted',
            'common practice',
            'minimum necessary',
            'does not apply',
            'opportunity to',
            'family',
            'treatment',
            'payment',
            'operations'
        ]
        
        primary_indicators = [
            'prohibited',
            'may not',
            'except as',
            'authorization required',
            'consent required',
            'violation',
            'must obtain',
            'is required'
        ]
        
        procedural_keyword_boost = sum(
            0.1 for ind in procedural_indicators if ind in query_lower
        )
        
        primary_keyword_boost = sum(
            0.1 for ind in primary_indicators if ind in query_lower
        )
        
        procedural_score += procedural_keyword_boost
        primary_score += primary_keyword_boost
        
        print(f"🔀 Routing scores:")
        print(f"   - Procedural: {procedural_score:.2f}")
        print(f"   - Primary: {primary_score:.2f}")
        
        # Step 3: Route based on scores
        # Default to procedural if close or unclear (Tier 1 is faster)
        if procedural_score >= primary_score * 0.8:  # Within 80%
            tier = "procedural"
            relevant = self._get_relevant_policies(query_lower, self.procedural_policies)
            print(f"   → Routed to PROCEDURAL tier ({len(relevant)} policies)")
        else:
            tier = "primary"
            relevant = self._get_relevant_policies(query_lower, self.primary_policies)
            print(f"   → Routed to PRIMARY tier ({len(relevant)} policies)")
        
        return tier, relevant
    
    def _score_against_policies(self, query: str, policies: List[Dict], 
                                keyword_index: Dict) -> float:
        """
        Score how well query matches policies
        
        Returns:
            Score from 0.0 to 1.0+
        """
        
        if not policies or not keyword_index:
            return 0.0
        
        query_words = set(w.strip('.,;:!?()[]{}') for w in query.split())
        query_words = {w for w in query_words if len(w) > 3}
        
        if not query_words:
            return 0.0
        
        # Count how many query words appear in policy index
        matches = sum(1 for word in query_words if word in keyword_index)
        
        return matches / len(query_words) if query_words else 0.0
    
    def _get_relevant_policies(self, query: str, policies: List[Dict], 
                              top_k: int = 20) -> List[Dict]:
        """
        Get top-k most relevant policies for the query
        
        Uses keyword overlap scoring
        """
        
        query_words = set(w.strip('.,;:!?()[]{}').lower() for w in query.split())
        query_words = {w for w in query_words if len(w) > 3}
        
        scored = []
        
        for policy in policies:
            # Get policy text
            text = policy.get('text', '') or policy.get('description', '') or policy.get('natural_language', '')
            text_lower = text.lower()
            text_words = set(w.strip('.,;:!?()[]{}') for w in text_lower.split())
            text_words = {w for w in text_words if len(w) > 3}
            
            # Calculate overlap
            overlap = len(query_words & text_words)
            
            if overlap > 0:
                # Boost score if section appears in query
                section = policy.get('section', '')
                if section and section.replace('§', '').strip() in query:
                    overlap += 5
                
                scored.append((overlap, policy))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)
        
        return [p for _, p in scored[:top_k]]
    
    def get_procedural_text_for_llm(self, query: str, max_policies: int = 15) -> str:
        """
        Get procedural policy text formatted for LLM
        
        Returns:
            Formatted string with top procedural policies relevant to query
        """
        
        relevant = self._get_relevant_policies(
            query.lower(), 
            self.procedural_policies, 
            max_policies
        )
        
        if not relevant:
            return "No procedural policies found matching this query."
        
        texts = []
        for i, policy in enumerate(relevant, 1):
            section = policy.get('section', 'Unknown')
            title = policy.get('title', '')
            text = policy.get('text', '') or policy.get('description', '') or policy.get('natural_language', '')
            
            # Truncate very long texts
            if len(text) > 500:
                text = text[:500] + "..."
            
            header = f"{i}. [{section}]"
            if title:
                header += f" {title}"
            
            texts.append(f"{header}\n{text}")
        
        return "\n\n".join(texts)
    
    def get_primary_text_for_llm(self, query: str, max_policies: int = 15) -> str:
        """
        Get primary policy text formatted for LLM
        
        Returns:
            Formatted string with top primary policies relevant to query
        """
        
        relevant = self._get_relevant_policies(
            query.lower(),
            self.primary_policies,
            max_policies
        )
        
        if not relevant:
            return "No primary policies found matching this query."
        
        texts = []
        for i, policy in enumerate(relevant, 1):
            section = policy.get('section', 'Unknown')
            title = policy.get('title', '')
            text = policy.get('text', '') or policy.get('description', '') or policy.get('natural_language', '')
            
            # Truncate very long texts
            if len(text) > 500:
                text = text[:500] + "..."
            
            header = f"{i}. [{section}]"
            if title:
                header += f" {title}"
            
            texts.append(f"{header}\n{text}")
        
        return "\n\n".join(texts)
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about loaded policies"""
        return {
            "procedural_count": len(self.procedural_policies),
            "primary_count": len(self.primary_policies),
            "procedural_keywords": len(self.procedural_keywords),
            "primary_keywords": len(self.primary_keywords)
        }
