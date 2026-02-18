
"""
UPDATED RAG IMPLEMENTATION
Uses CFR XML parser instead of hardcoded CSV database

This fixes the issue where RAG was still using old HIPAA-0567 style IDs
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import time
from typing import List, Dict
import pandas as pd
import csv
import hashlib
from io import StringIO
import streamlit as st
import json
import re

# ============================================================================
# IMPORT CFR PARSER
# ============================================================================

def get_rag_policy_database(xml_path: str = "cfr/title45.xml") -> List[Dict]:
    """
    Get policy database for RAG using CFR XML parser
    
    This replaces the old hardcoded CSV database
    """
    
    try:
        # Try to import comprehensive CFR parser
        from utils.cfr_parser import load_policy_database
        
        # Load HIPAA policies only (Parts 160, 162, 164)
        policies = load_policy_database(mode="hipaa_only", xml_path=xml_path)
        
        print(f"✅ RAG loaded {len(policies)} policies from CFR XML")
        return policies
    
    except ImportError:
        print("⚠️ CFR parser not found, trying simple XML parser")
        try:
            from utils.cfr_parser import load_policy_database
            policies = load_policy_database(mode="hipaa_only")
            print(f"✅ RAG loaded {len(policies)} policies from XML")
            return policies
        except:
            pass
    
    except FileNotFoundError:
        print(f"⚠️ XML file not found: {xml_path}")
    
    except Exception as e:
        print(f"⚠️ Error loading from XML: {e}")
    
    # Fallback to minimal database
    print("⚠️ Using fallback RAG database")
    return get_fallback_rag_database()

def get_fallback_rag_database() -> List[Dict]:
    """
    Minimal fallback database if XML parsing fails
    
    Uses standard HIPAA-0 to HIPAA-N naming (not HIPAA-0567)
    """
    return [
        {
            "policy_id": "HIPAA-0",
            "section": "§164.502(a)(1)",
            "title": "Standard: Uses and disclosures of protected health information",
            "description": "General permitted uses and disclosures",
            "text": "A covered entity may not use or disclose protected health information, except as permitted or required by this subpart or by subpart C of part 160 of this subchapter. (i) Permitted uses and disclosures. A covered entity is permitted to use or disclose protected health information as follows: (A) To the individual; (B) For treatment, payment, or health care operations, as permitted by and in compliance with §164.506; (C) Incident to a use or disclosure otherwise permitted or required by this subpart, provided that the covered entity has complied with the applicable requirements of §164.502(b), §164.514(d), and §164.530(c) with respect to such otherwise permitted or required use or disclosure."
        },
        {
            "policy_id": "HIPAA-1",
            "section": "§164.506(a)",
            "title": "Consent for uses and disclosures to carry out treatment, payment, or health care operations",
            "description": "Consent not required for TPO",
            "text": "Standard: Consent for uses and disclosures permitted. (a) A covered entity may use or disclose protected health information for treatment, payment, or health care operations with the individual's consent. A covered entity may condition treatment, payment, enrollment in the health plan, or eligibility for benefits on the provision of such consent, except as prohibited under §164.506(b)(4)."
        },
        {
            "policy_id": "HIPAA-2",
            "section": "§164.508(a)(1)",
            "title": "Uses and disclosures for which an authorization is required",
            "description": "Authorization required for non-TPO uses",
            "text": "Standard: Authorizations for uses and disclosures. (a)(1) Authorization required: General rule. Except as otherwise permitted or required by this subchapter, a covered entity may not use or disclose protected health information without an authorization that is valid under this section. When a covered entity obtains or receives a valid authorization for its use or disclosure of protected health information, such use or disclosure must be consistent with such authorization."
        },
        {
            "policy_id": "HIPAA-3",
            "section": "§164.510(b)",
            "title": "Uses and disclosures for involvement in the individual's care",
            "description": "Disclosure to family members and others involved in care",
            "text": "Standard: Uses and disclosures for involvement in the individual's care and notification purposes. A covered entity may, in accordance with §164.510(b)(2) or (b)(3), disclose to a family member, other relative, or a close personal friend of the individual, or any other person identified by the individual, the protected health information directly relevant to such person's involvement with the individual's care or payment related to the individual's health care."
        },
        {
            "policy_id": "HIPAA-4",
            "section": "§164.512(i)",
            "title": "Uses and disclosures for research purposes",
            "description": "Research disclosures with authorization or IRB waiver",
            "text": "Standard: Uses and disclosures for research purposes. A covered entity may use or disclose protected health information for research purposes pursuant to a written authorization that meets the requirements of §164.508, or pursuant to a waiver, in whole or in part, of the authorization requirement under §164.512(i)(1)(i) obtained by an IRB or privacy board."
        }
    ]

# ============================================================================
# UPDATED RAG EXPERIMENT
# ============================================================================

def experiment_rag(query: str, client, xml_path: str = "cfr/title45.xml") -> dict:
    """
    Updated RAG experiment using CFR XML policies
    
    Args:
        query: User's compliance question
        client: Anthropic client
        xml_path: Path to CFR XML file
    
    Returns:
        Experiment results
    """
    
    start = time.time()
    steps = ["🔍 Retrieving HIPAA policies using hybrid search (semantic + keyword)"]
    
    try:
        # STEP 1: Load policies from CFR XML
        policies = get_rag_policy_database(xml_path)
        
        if not policies:
            return {
                "name": "RAG (Retrieval-Augmented Generation)",
                "answer": "Error: No policies loaded",
                "duration": time.time() - start,
                "steps": steps + ["❌ Failed to load policies"],
                "method": "Retrieval-Augmented Generation (Failed)"
            }
        
        # STEP 2: Hybrid retrieval (semantic + keyword)
        retrieved_policies = hybrid_retrieve(query, policies, top_k=5)
        
        steps.append(f"✅ Retrieved {len(retrieved_policies)} policies using hybrid search")
        steps.append("")
        
        # Show retrieved policies
        for i, (policy, scores) in enumerate(retrieved_policies, 1):
            sim_score = scores['combined']
            sem_score = scores['semantic']
            kw_score = scores['keyword']
            
            steps.append(
                f"📌 {policy['policy_id']} — {policy['title'][:50]}\n"
                f"   Section: {policy['section']}\n"
                f"   Similarity: {sim_score:.2f} (semantic: {sem_score:.2f}, keyword: {kw_score:.2f})\n"
                f"   Text: {policy['text'][:100]}..."
            )
        
        # STEP 3: Generate answer with context
        context = "\n\n".join([
            f"Policy {p['policy_id']} ({p['section']}): {p['text']}"
            for p, _ in retrieved_policies
        ])
        
        prompt = f"""Based on these HIPAA policies, answer the compliance question.

POLICIES:
{context}

QUESTION: {query}

Provide:
1. Direct YES or NO answer
2. Brief explanation
3. Cite the relevant HIPAA section
4. Actionable guidance if applicable

Answer:"""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.content[0].text
        
        # STEP 4: Parse verdict
        answer_upper = answer.upper()
        if "YES" in answer_upper[:50] and "NO" not in answer_upper[:50]:
            verdict = "✅ COMPLIANT"
        elif "NO" in answer_upper[:50]:
            verdict = "❌ VIOLATION"
        else:
            verdict = "⚠️ UNCLEAR"
        
        return {
            "name": "RAG (Retrieval-Augmented Generation)",
            "answer": answer,
            "duration": time.time() - start,
            "steps": steps,
            "verdict": verdict,
            "method": "Retrieval-Augmented Generation (Hybrid)",
            "retrieved_policies": [p['policy_id'] for p, _ in retrieved_policies],
            "policy_count": len(policies),
            "source": "CFR XML"
        }
    
    except Exception as e:
        import traceback
        return {
            "name": "RAG (Retrieval-Augmented Generation)",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}", traceback.format_exc()],
            "verdict": "⚠️ ERROR",
            "method": "RAG (Failed)"
        }

def hybrid_retrieve(query: str, policies: List[Dict], top_k: int = 5) -> List[tuple]:
    """
    Hybrid retrieval: Semantic embeddings + BM25 keyword matching
    
    Returns:
        List of (policy, scores) tuples
    """
    
    # Load embedding model
    print("🔄 Loading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    
    # Create policy texts
    policy_texts = [
        f"{p.get('title', '')} {p.get('description', '')} {p.get('text', '')}"
        for p in policies
    ]
    
    # Encode policies
    print("🔄 Encoding policies...")
    policy_embeddings = model.encode(policy_texts, show_progress_bar=False)
    query_embedding = model.encode([query])[0]
    
    # Semantic similarity
    semantic_scores = np.dot(policy_embeddings, query_embedding)
    semantic_scores = (semantic_scores - semantic_scores.min()) / (semantic_scores.max() - semantic_scores.min() + 1e-8)
    
    # BM25 keyword matching
    tokenized_policies = [text.lower().split() for text in policy_texts]
    tokenized_query = query.lower().split()
    
    bm25 = BM25Okapi(tokenized_policies)
    keyword_scores = bm25.get_scores(tokenized_query)
    keyword_scores = (keyword_scores - keyword_scores.min()) / (keyword_scores.max() - keyword_scores.min() + 1e-8)
    
    # Hybrid score (70% semantic, 30% keyword)
    combined_scores = 0.7 * semantic_scores + 0.3 * keyword_scores
    
    # Get top-k
    top_indices = np.argsort(combined_scores)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        results.append((
            policies[idx],
            {
                'semantic': float(semantic_scores[idx]),
                'keyword': float(keyword_scores[idx]),
                'combined': float(combined_scores[idx])
            }
        ))
    
    return results

class RAGPolicyExporter:
    """Export policies to RAG-friendly CSV format"""
    
    @staticmethod
    def generate_policy_id(regulation: str, section: str) -> str:
        """Generate unique policy ID"""
        section_clean = section.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')
        hash_suffix = hashlib.md5(f"{regulation}{section}".encode()).hexdigest()[:6]
        return f"{regulation.upper()}-{section_clean}-{hash_suffix}"
    
    @staticmethod
    def extract_keywords(statement: str, title: str) -> list:
        """Extract keywords from policy statement"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
                     'may', 'shall', 'must', 'should', 'can', 'could', 'will', 'would'}
        
        text = (statement + " " + title).lower()
        words = re.findall(r'\b[a-z]{4,}\b', text)
        
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:10]]
    
    @staticmethod
    def generate_rag_csv(results: dict) -> str:
        """
        Generate RAG CSV from processing results
        
        Args:
            results: Dict with keys: 'regulation', 'policies'
                     where 'policies' is a list of dicts with:
                     - 'section': str
                     - 'title': str
                     - 'statement': str
                     - 'fotl_formula': str
                     - 'conditions': list (optional)
                     - 'action': str (optional)
        """
        
        rows = []
        regulation = results.get('regulation', 'UNKNOWN')
        policies = results.get('policies', [])
        
        for policy in policies:
            policy_id = RAGPolicyExporter.generate_policy_id(
                regulation, 
                policy.get('section', 'N/A')
            )
            
            keywords = RAGPolicyExporter.extract_keywords(
                policy.get('statement', ''),
                policy.get('title', '')
            )
            
            row = {
                'policy_id': policy_id,
                'regulation': regulation,
                'section': policy.get('section', ''),
                'title': policy.get('title', ''),
                'description': policy.get('statement', ''),
                'fotl_formula': policy.get('fotl_formula', ''),
                'keywords': ','.join(keywords),
                'conditions': ','.join(policy.get('conditions', [])),
                'action': policy.get('action', ''),
                'parent_id': '',
                'created_at': pd.Timestamp.now().isoformat()
            }
            
            rows.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(rows)
        
        # Convert to CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_ALL)
        
        return csv_buffer.getvalue()

# ============================================
# RAG SEARCH FUNCTIONS
# ============================================

class RAGPolicySearch:
    """Search policies using RAG approach"""
    
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
    
    def search_by_keywords(self, query: str, top_k: int = 5) -> pd.DataFrame:
        """Keyword-based search"""
        query_lower = query.lower()
        
        # Score each policy
        scores = []
        for idx, row in self.df.iterrows():
            score = 0
            
            # Check keywords
            keywords = row['keywords'].split(',')
            for kw in keywords:
                if kw in query_lower:
                    score += 2
            
            # Check title
            if any(word in row['title'].lower() for word in query_lower.split()):
                score += 3
            
            # Check description
            if any(word in row['description'].lower() for word in query_lower.split()):
                score += 1
            
            scores.append(score)
        
        self.df['relevance_score'] = scores
        
        return self.df[self.df['relevance_score'] > 0].nlargest(top_k, 'relevance_score')
    
    def search_by_section(self, section: str) -> pd.DataFrame:
        """Search by section number"""
        return self.df[self.df['section'].str.contains(section, case=False)]
    
    def search_by_regulation(self, regulation: str) -> pd.DataFrame:
        """Filter by regulation"""
        return self.df[self.df['regulation'].str.upper() == regulation.upper()]

# ============================================
# INTEGRATION WITH STREAMLIT
# ============================================

def add_rag_export_to_results(results: dict):
    """Add RAG export options to Streamlit UI"""
    
    st.markdown("---")
    st.markdown("## 🔍 RAG Database Export")
    st.info("Export policies in searchable format for Retrieval-Augmented Generation (RAG)")
    
    # Generate RAG CSV
    rag_csv = RAGPolicyExporter.generate_rag_csv(results)
    
    # Generate complete session export
    complete_export = RAGPolicyExporter.generate_complete_session_export(results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            label="📊 RAG CSV",
            data=rag_csv,
            file_name=f"{results['regulation'].lower()}_rag.csv",
            mime="text/csv",
            help="Searchable policy database",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📄 Type System",
            data=results['type_system'],
            file_name=f"{results['regulation'].lower()}_types.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            label="📜 Policy File",
            data=results['policy_file'],
            file_name=f"{results['regulation'].lower()}_generated.policy",
            mime="text/plain",
            use_container_width=True
        )
    
    with col4:
        st.download_button(
            label="💾 Complete Session",
            data=json.dumps(complete_export, indent=2),
            file_name=f"{results['regulation'].lower()}_session.json",
            mime="application/json",
            help="Everything for reproducibility",
            use_container_width=True
        )
    
    # Preview RAG CSV
    with st.expander("👁️ Preview RAG CSV"):
        df = pd.read_csv(StringIO(rag_csv))
        st.dataframe(df[['policy_id', 'section', 'title', 'keywords']], use_container_width=True)
        
        st.markdown("**Sample Row:**")
        if len(df) > 0:
            sample = df.iloc[0].to_dict()
            st.json(sample)
    
    # RAG Search Demo
    with st.expander("🔍 Test RAG Search"):
        search_query = st.text_input("Search query", "consent")
        
        if search_query:
            searcher = RAGPolicySearch(StringIO(rag_csv))
            results_df = searcher.search_by_keywords(search_query, top_k=3)
            
            if len(results_df) > 0:
                st.success(f"Found {len(results_df)} matching policies")
                for _, row in results_df.iterrows():
                    st.markdown(f"**{row['section']}** - {row['title']} (Score: {row['relevance_score']})")
            else:
                st.warning("No matches found")

# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================

def integration_instructions():
    """
    How to integrate this into your existing code
    """
    
    return """
# In your main streamlit app or experiment runner:

# OLD (using hardcoded CSV database):
def experiment_rag(query, client):
    # Old implementation with HIPAA-0567 style IDs
    pass

# NEW (using CFR XML):
from rag_updated import experiment_rag_updated

def experiment_rag(query, client):
    return experiment_rag_updated(
        query=query, 
        client=client,
        xml_path="cfr/title45.xml"  # or wherever your XML is
    )

# That's it! Now RAG uses the same CFR XML database as everything else
# Policy IDs will be HIPAA-0, HIPAA-1, etc. (matching OCaml Précis)
"""

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    from anthropic import Anthropic
    import os
    
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Test query
    query = "Can my grandma get my x-ray scan?"
    
    print("🧪 Testing Updated RAG Implementation")
    print("="*70)
    
    result = experiment_rag(query, client)
    
    print(f"\n📝 Query: {query}")
    print(f"\n🎯 Verdict: {result['verdict']}")
    print(f"\n⏱️ Duration: {result['duration']:.1f}s")
    print(f"\n📚 Retrieved Policies: {result.get('retrieved_policies', [])}")
    print(f"\n💬 Answer:\n{result['answer']}")
    
    print(f"\n🔧 Processing Steps:")
    for step in result['steps']:
        print(f"   {step}")
