"""
Integrated Two-Tier Verifier

Combines:
1. JSON policy classification (procedural vs primary)
2. Pattern matching (fast, common cases)
3. LLM classification (flexible, edge cases)
4. OCaml FOTL verification (rigorous, substantive rules)

Architecture:
- Tier 1A: Hardcoded pattern matching (60-70% coverage, <100ms)
- Tier 1B: LLM + procedural JSON (15-20% coverage, 1-2s)
- Tier 2: OCaml + primary FOTL (10-20% coverage, 5-10s)
"""

import json
import re
from typing import List, Dict, Optional
from anthropic import Anthropic
from dataclasses import dataclass
from enum import Enum

from utils.policy_router import PolicyRouter


class VerificationTier(Enum):
    """Which tier resolved the verification"""
    TIER_1A_PATTERN = "tier_1a_pattern"
    TIER_1B_PROCEDURAL = "tier_1b_procedural"
    TIER_2_FORMAL = "tier_2_formal"


@dataclass
class ProceduralException:
    """Represents a procedural exception that allows disclosure"""
    name: str
    cite: str
    description: str
    applies: bool = False
    confidence: float = 0.0
    source: str = "pattern"  # "pattern" or "llm"


@dataclass
class VerificationResult:
    """Complete verification result with tier information"""
    compliant: bool
    tier: VerificationTier
    confidence: float
    explanation: str
    policy_citations: List[str]
    procedural_exception: Optional[ProceduralException] = None
    formal_result: Optional[Dict] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class IntegratedTwoTierVerifier:
    """
    Complete two-tier verification system integrating:
    - JSON policy classification
    - Hardcoded pattern matching
    - LLM procedural classification
    - OCaml FOTL formal verification
    """
    
    def __init__(self,
                 client: Anthropic,
                 ocaml_verifier=None,
                 procedural_json: str = "policies/procedural_policies.json",
                 primary_json: str = "policies/primary_policies.json",
                 primary_fotl: str = "policies/HIPAA_PRIMARY.policy",
                 procedural_fotl: str = "policies/HIPAA_PROCEDURAL.policy"):
        
        self.client = client
        self.ocaml_verifier = ocaml_verifier
        self.primary_fotl = primary_fotl
        self.procedural_fotl = procedural_fotl
        
        # Initialize policy router (uses JSON files)
        self.router = PolicyRouter(procedural_json, primary_json)
        
        # Load hardcoded patterns for common cases
        self.hardcoded_patterns = self._load_hardcoded_patterns()
        
        # LLM result cache
        self.llm_cache = {}
        
        print("✅ Integrated Two-Tier Verifier initialized")
    
    def verify(self, query: str, facts: List[List], formula: str) -> VerificationResult:
        """
        Complete two-tier verification pipeline
        
        Flow:
        1. Route query using JSON classification
        2. If procedural → Try Tier 1A pattern matching
        3. If no match → Try Tier 1B LLM classification
        4. If still no match OR primary → Tier 2 OCaml verification
        
        Args:
            query: Natural language compliance question
            facts: Extracted predicates
            formula: First-order logic formula
            
        Returns:
            VerificationResult with tier and confidence
        """
        
        print(f"\n{'='*60}")
        print(f"🔍 VERIFICATION PIPELINE")
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"Facts: {len(facts)} extracted")
        
        # ========================================
        # STEP 1: Route using JSON classification
        # ========================================
        
        tier, relevant_policies = self.router.route_query(query, facts)
        
        # ========================================
        # TIER 1: PROCEDURAL CHECKS
        # ========================================
        
        if tier == "procedural":
            print(f"\n{'─'*60}")
            print(f"🎯 TIER 1: Procedural Exception Checks")
            print(f"{'─'*60}")
            
            # Try Tier 1A: Pattern matching (fast)
            print("Tier 1A: Checking hardcoded patterns...")
            pattern_result = self._check_hardcoded_patterns(query, facts)
            
            if pattern_result.applies and pattern_result.confidence >= 0.70:
                print(f"✅ Tier 1A: Pattern matched!")
                print(f"   Exception: {pattern_result.name}")
                print(f"   Confidence: {pattern_result.confidence:.2%}")
                
                return VerificationResult(
                    compliant=True,
                    tier=VerificationTier.TIER_1A_PATTERN,
                    confidence=pattern_result.confidence,
                    explanation=pattern_result.description,
                    policy_citations=[pattern_result.cite],
                    procedural_exception=pattern_result
                )
            else:
                print(f"   No pattern match (confidence: {pattern_result.confidence:.2%})")
            
            # Try Tier 1B: LLM classification (flexible)
            print("\nTier 1B: Checking with LLM + procedural JSON...")
            llm_result = self._check_procedural_with_llm(query, facts, relevant_policies)
            
            if llm_result.applies and llm_result.confidence >= 0.65:
                print(f"✅ Tier 1B: LLM found exception!")
                print(f"   Exception: {llm_result.name}")
                print(f"   Confidence: {llm_result.confidence:.2%}")
                
                return VerificationResult(
                    compliant=True,
                    tier=VerificationTier.TIER_1B_PROCEDURAL,
                    confidence=llm_result.confidence,
                    explanation=llm_result.description,
                    policy_citations=[llm_result.cite],
                    procedural_exception=llm_result
                )
            else:
                print(f"   No LLM match (confidence: {llm_result.confidence:.2%})")
            
            print("\n   → No procedural exception found, proceeding to Tier 2...")
        
        # ========================================
        # TIER 2: FORMAL VERIFICATION
        # ========================================
        
        print(f"\n{'─'*60}")
        print(f"⚙️ TIER 2: OCaml Formal Verification")
        print(f"{'─'*60}")
        
        if self.ocaml_verifier is None:
            print("❌ OCaml verifier not available")
            return self._heuristic_fallback(query, facts)
        
        # Filter facts for formal verification
        filtered_facts = self._filter_facts_for_formal(facts)
        print(f"Filtered {len(facts)} → {len(filtered_facts)} facts for OCaml")
        
        # Call OCaml with PRIMARY.policy
        print(f"Calling OCaml with {self.primary_fotl}...")
        formal_result = self.ocaml_verifier.verify(formula, filtered_facts)
        
        return self._interpret_formal_result(formal_result, query, facts)
    
    def _load_hardcoded_patterns(self) -> List[Dict]:
        """
        Hardcoded patterns for common procedural exceptions
        
        These are the most frequent cases that can be matched instantly
        without LLM or OCaml overhead
        """
        return [
            {
                "name": "Treatment Use (Internal)",
                "cite": "45 CFR §164.506(c)(1)",
                "keywords": ["treatment", "use", "care", "patient", "records"],
                "min_keywords": 1,
                "pattern": {
                    "entity_type": ["covered_entity", "provider", "hospital", "clinic", "pharmacy"],
                    "purpose": ["treatment", "@Treatment", "care"]
                },
                "confidence_base": 0.95,
                "description": (
                    "A covered entity may use protected health information "
                    "for its own treatment purposes without patient authorization "
                    "(45 CFR §164.506(c)(1))."
                )
            },
            {
                "name": "Treatment Referral",
                "cite": "45 CFR §164.506(c)(2)",
                "keywords": ["treatment", "referral", "specialist", "consult", "refer"],
                "min_keywords": 1,
                "pattern": {
                    "entity_type": ["provider", "hospital", "clinic"],
                    "recipient_type": ["specialist", "provider", "doctor", "physician"],
                    "purpose": ["treatment", "@Treatment", "referral"]
                },
                "confidence_base": 0.98,
                "description": (
                    "Covered entities may disclose PHI for treatment activities "
                    "of another healthcare provider without authorization "
                    "(45 CFR §164.506(c)(2))."
                )
            },
            {
                "name": "Family Prescription Pickup",
                "cite": "45 CFR §164.510(b)(3)",
                "keywords": ["family", "prescription", "pick", "medication", "relative"],
                "min_keywords": 2,
                "pattern": {
                    "entity_type": ["pharmacy", "provider"],
                    "recipient_type": ["family", "relative", "spouse", "parent"],
                    "phi_type": ["prescription", "medication"],
                    "purpose": ["pickup", "pick up"]
                },
                "confidence_base": 0.95,
                "description": (
                    "Professional judgment allows family members to pick up "
                    "prescriptions, medical supplies, or X-rays without explicit "
                    "authorization (45 CFR §164.510(b)(3))."
                )
            },
            {
                "name": "Payment Activities",
                "cite": "45 CFR §164.506(c)(3)",
                "keywords": ["payment", "billing", "insurance", "claim", "bill"],
                "min_keywords": 1,
                "pattern": {
                    "purpose": ["payment", "@Payment", "billing"]
                },
                "confidence_base": 0.95,
                "description": (
                    "Covered entities may disclose PHI for payment purposes "
                    "without patient authorization (45 CFR §164.506(c)(3))."
                )
            },
            {
                "name": "Healthcare Operations",
                "cite": "45 CFR §164.506(c)(4)",
                "keywords": ["operations", "quality", "improvement", "accreditation"],
                "min_keywords": 1,
                "pattern": {
                    "purpose": ["@HealthcareOperations", "operations", "quality"]
                },
                "confidence_base": 0.85,
                "description": (
                    "Covered entities may use PHI for healthcare operations "
                    "including quality assessment and improvement "
                    "(45 CFR §164.506(c)(4))."
                )
            },
            {
                "name": "Public Health Reporting",
                "cite": "45 CFR §164.512(b)",
                "keywords": ["public health", "disease", "reporting", "outbreak", "cdc"],
                "min_keywords": 2,
                "pattern": {
                    "recipient_type": ["public_health", "health_department", "cdc"],
                    "purpose": ["@PublicHealth", "disease", "reporting"]
                },
                "confidence_base": 0.98,
                "description": (
                    "Covered entities may disclose PHI to public health authorities "
                    "for public health activities including disease surveillance "
                    "(45 CFR §164.512(b))."
                )
            }
        ]
    
    def _check_hardcoded_patterns(self, query: str, facts: List[List]) -> ProceduralException:
        """
        Check hardcoded pattern exceptions (Tier 1A)
        
        Fast pattern matching using keyword and fact analysis
        """
        
        query_lower = query.lower()
        best_match = None
        best_confidence = 0.0
        
        for pattern_def in self.hardcoded_patterns:
            # Keyword matching
            keywords = pattern_def["keywords"]
            keyword_matches = sum(1 for kw in keywords if kw in query_lower)
            
            if keyword_matches < pattern_def["min_keywords"]:
                continue  # Not enough keywords
            
            # Pattern matching in facts
            pattern_score = self._match_pattern_in_facts(
                pattern_def["pattern"],
                facts,
                query_lower
            )
            
            # Calculate combined confidence
            keyword_weight = 0.4
            pattern_weight = 0.6
            
            keyword_conf = min(1.0, keyword_matches / len(keywords))
            
            confidence = (
                keyword_weight * keyword_conf +
                pattern_weight * pattern_score
            ) * pattern_def["confidence_base"]
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_match = ProceduralException(
                    name=pattern_def["name"],
                    cite=pattern_def["cite"],
                    description=pattern_def["description"],
                    applies=confidence >= 0.70,
                    confidence=confidence,
                    source="pattern"
                )
        
        return best_match or ProceduralException(
            name="None", cite="", description="",
            applies=False, confidence=0.0, source="pattern"
        )
    
    def _match_pattern_in_facts(self, pattern: Dict, facts: List[List], 
                                query_lower: str) -> float:
        """
        Match pattern requirements against extracted facts
        
        Returns:
            Score from 0.0 to 1.0
        """
        
        total_checks = 0
        matches = 0
        
        # Build fact index
        fact_predicates = {f[0]: f[1:] for f in facts if len(f) >= 2}
        
        # Check entity_type
        if "entity_type" in pattern:
            total_checks += 1
            entity = fact_predicates.get('coveredEntity', [''])[0]
            if any(self._fuzzy_match(et, entity) for et in pattern["entity_type"]):
                matches += 1
        
        # Check purpose
        if "purpose" in pattern:
            total_checks += 1
            
            # Check in facts
            for fact in facts:
                if fact[0] in ['disclose', 'permittedUseOrDisclosure'] and len(fact) >= 5:
                    purpose = fact[4]
                    if any(self._fuzzy_match(p, purpose) for p in pattern["purpose"]):
                        matches += 1
                        break
            
            # Also check in query
            if any(p.lower().replace('@', '') in query_lower for p in pattern["purpose"]):
                matches += 0.5  # Partial credit
        
        # Check recipient_type
        if "recipient_type" in pattern:
            total_checks += 1
            for fact in facts:
                if fact[0] == 'disclose' and len(fact) >= 3:
                    recipient = fact[2]
                    if any(self._fuzzy_match(rt, recipient) for rt in pattern["recipient_type"]):
                        matches += 1
                        break
        
        # Check PHI type
        if "phi_type" in pattern:
            total_checks += 1
            if any(phi_type in query_lower for phi_type in pattern["phi_type"]):
                matches += 1
        
        return matches / total_checks if total_checks > 0 else 0.0
    
    def _fuzzy_match(self, pattern: str, text: str) -> bool:
        """Fuzzy string matching"""
        pattern_clean = pattern.lower().replace('_', '').replace('-', '')
        text_clean = str(text).lower().replace('_', '').replace('-', '')
        return pattern_clean in text_clean or text_clean in pattern_clean
    
    def _check_procedural_with_llm(self, query: str, facts: List[List],
                                  relevant_policies: List[Dict]) -> ProceduralException:
        """
        Check procedural exceptions using LLM + JSON policies (Tier 1B)
        
        More flexible than pattern matching, can handle nuanced cases
        """
        
        # Check cache
        cache_key = (query, str(facts))
        if cache_key in self.llm_cache:
            return self.llm_cache[cache_key]
        
        # Get procedural policy text
        policy_text = self.router.get_procedural_text_for_llm(query, max_policies=15)
        
        if not policy_text or "No procedural policies" in policy_text:
            return ProceduralException(
                name="None", cite="", description="",
                applies=False, confidence=0.0, source="llm"
            )
        
        prompt = f"""You are a HIPAA compliance expert. Determine if this scenario matches a PROCEDURAL exception.

Query: {query}
Facts: {facts}

PROCEDURAL POLICIES (these allow disclosure without explicit authorization):
{policy_text}

TASK:
Procedural policies typically contain language like:
- "may use or disclose"
- "is permitted to"
- "professional judgment"
- "does not require authorization"
- "common practice"

Does the query match ANY procedural policy above?

Output ONLY valid JSON:
{{
    "matches": true/false,
    "exception_name": "Brief name" or null,
    "section": "164.XXX" or null,
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation why it matches/doesn't match"
}}"""
        
        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from response
            text = response.content[0].text.strip()
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            
            if json_match:
                result = json.loads(json_match.group())
                
                exception = ProceduralException(
                    name=result.get('exception_name', 'LLM-Detected Exception'),
                    cite=f"45 CFR §{result.get('section', 'Unknown')}",
                    description=result.get('reasoning', ''),
                    applies=result.get('matches', False),
                    confidence=result.get('confidence', 0.0),
                    source="llm"
                )
                
                # Cache result
                self.llm_cache[cache_key] = exception
                
                return exception
        
        except Exception as e:
            print(f"   ⚠️ LLM procedural check failed: {e}")
        
        return ProceduralException(
            name="None", cite="", description="",
            applies=False, confidence=0.0, source="llm"
        )
    
    def _filter_facts_for_formal(self, facts: List[List]) -> List[List]:
        """
        Filter facts for formal verification
        
        Remove conclusion predicates (hasAuthorization, permittedUseOrDisclosure)
        Keep only factual predicates for OCaml
        """
        
        factual_predicates = {
            'coveredEntity',
            'protectedHealthInfo',
            'publicHealthAuthority',
            'businessAssociate',
            'disclose',
            'requiredByLaw'
        }
        
        return [f for f in facts if len(f) >= 2 and f[0] in factual_predicates]
    
    def _interpret_formal_result(self, formal_result: Dict, query: str,
                                facts: List[List]) -> VerificationResult:
        """
        Interpret OCaml Précis formal verification result
        """
        
        if not formal_result.get('success', False):
            print(f"❌ OCaml execution failed: {formal_result.get('error', 'Unknown error')}")
            
            # Heuristic fallback
            return self._heuristic_fallback(query, facts)
        
        verified = formal_result.get('verified', False)
        evaluations = formal_result.get('evaluations', [])
        violations = formal_result.get('violations', [])
        
        print(f"{'✅' if verified else '❌'} OCaml result: {'COMPLIANT' if verified else 'VIOLATION'}")
        if evaluations:
            print(f"   Evaluations: {len(evaluations)}")
        if violations:
            print(f"   Violations: {len(violations)}")
        
        # Extract citations
        citations = []
        for eval_item in evaluations:
            if 'policy_id' in eval_item:
                citations.append(eval_item['policy_id'])
        
        return VerificationResult(
            compliant=verified,
            tier=VerificationTier.TIER_2_FORMAL,
            confidence=0.95 if verified else 0.90,
            explanation=(
                "Formal verification confirms compliance with HIPAA primary policies."
                if verified else
                f"Formal verification found {len(violations)} policy violation(s)."
            ),
            policy_citations=citations,
            formal_result=formal_result
        )
    
    def _heuristic_fallback(self, query: str, facts: List[List]) -> VerificationResult:
        """
        Heuristic fallback when OCaml unavailable or fails
        
        Uses rule-based reasoning to approximate compliance
        """
        
        query_lower = query.lower()
        
        # Check for clear compliance indicators
        treatment_indicators = ['treatment', 'care', 'specialist', 'doctor', 'physician']
        payment_indicators = ['payment', 'billing', 'insurance', 'claim']
        operations_indicators = ['operations', 'quality', 'improvement']
        
        if any(ind in query_lower for ind in treatment_indicators):
            return VerificationResult(
                compliant=True,
                tier=VerificationTier.TIER_2_FORMAL,
                confidence=0.60,
                explanation=(
                    "Formal verification unavailable. Heuristic analysis "
                    "suggests treatment use which is generally permitted under "
                    "45 CFR §164.506(c)(1)."
                ),
                policy_citations=["45 CFR §164.506(c)(1)"],
                warnings=["OCaml Précis unavailable - using heuristic fallback"]
            )
        
        if any(ind in query_lower for ind in payment_indicators):
            return VerificationResult(
                compliant=True,
                tier=VerificationTier.TIER_2_FORMAL,
                confidence=0.60,
                explanation=(
                    "Formal verification unavailable. Heuristic analysis "
                    "suggests payment activities which are generally permitted."
                ),
                policy_citations=["45 CFR §164.506(c)(3)"],
                warnings=["OCaml Précis unavailable - using heuristic fallback"]
            )
        
        # Default to non-compliant if uncertain
        return VerificationResult(
            compliant=False,
            tier=VerificationTier.TIER_2_FORMAL,
            confidence=0.0,
            explanation="Unable to verify compliance - formal verification unavailable and no clear procedural exception applies.",
            policy_citations=[],
            warnings=["OCaml Précis unavailable - unable to verify"]
        )


def create_integrated_verifier(client: Anthropic, ocaml_verifier=None) -> IntegratedTwoTierVerifier:
    """
    Factory function to create integrated two-tier verifier
    
    Args:
        client: Anthropic client for LLM calls
        ocaml_verifier: Optional OCaml Précis verifier instance
        
    Returns:
        Configured IntegratedTwoTierVerifier
    """
    return IntegratedTwoTierVerifier(
        client=client,
        ocaml_verifier=ocaml_verifier,
        procedural_json="policies/procedural_policies.json",
        primary_json="policies/primary_policies.json",
        primary_fotl="policies/HIPAA_PRIMARY.policy",
        procedural_fotl="policies/HIPAA_PROCEDURAL.policy"
    )
