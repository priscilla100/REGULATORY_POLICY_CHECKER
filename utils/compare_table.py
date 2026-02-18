import streamlit as st
def determine_verdict_for_comparison(result: dict, query: str = "") -> str:
    """
    Comprehensive verdict determination for comparison table
    
    Returns: "✅ Compliant", "❌ Violation", or "⚠️ Unknown"
    
    This handles ALL experiment types:
    - Baseline (LLM only)
    - RAG (Retrieval + LLM)
    - Pipeline (Two-Tier)
    - Multi-Agent (Two-Tier)
    """
    
    query_lower = query.lower().strip() if query else ""
    
    # ================================================================
    # STEP 1: Check explicit compliance_status (Two-Tier systems)
    # ================================================================
    if 'compliance_status' in result:
        status = str(result['compliance_status']).upper()
        
        if "✅" in status or ("COMPLIANT" in status and "VIOLATION" not in status):
            return "✅ Compliant"
        elif "❌" in status or "VIOLATION" in status:
            return "❌ Violation"
        elif "⚠️" in status or "UNKNOWN" in status:
            return "⚠️ Unknown"
    
    # ================================================================
    # STEP 2: Check compliant field (Two-Tier systems)
    # ================================================================
    if 'compliant' in result:
        compliant = result['compliant']
        
        if compliant is True:
            return "✅ Compliant"
        elif compliant is False:
            # Check if OCaml failed (don't trust false negatives)
            formal_result = result.get('formal_result', {})
            if formal_result and not formal_result.get('success', False):
                # OCaml failed - check if procedural exception applied
                if result.get('procedural_exception'):
                    return "✅ Compliant"
                # OCaml failed, no exception - unknown
                return "⚠️ Unknown"
            return "❌ Violation"
    
    # ================================================================
    # STEP 3: Check verdict field (RAG, Baseline)
    # ================================================================
    if 'verdict' in result:
        verdict = str(result['verdict']).upper()
        
        if "✅" in verdict or "COMPLIANT" in verdict:
            return "✅ Compliant"
        elif "❌" in verdict or "VIOLATION" in verdict:
            return "❌ Violation"
        elif "⚠️" in verdict or "UNCLEAR" in verdict:
            # Try parsing answer
            return parse_answer_verdict(result, query_lower)
        else:
            return parse_answer_verdict(result, query_lower)
    
    # ================================================================
    # STEP 4: Check verified field (legacy Pipeline)
    # ================================================================
    if 'verified' in result:
        return "✅ Compliant" if result['verified'] else "❌ Violation"
    
    # ================================================================
    # STEP 5: Parse answer text (final fallback)
    # ================================================================
    return parse_answer_verdict(result, query_lower)


def parse_answer_verdict(result: dict, query_lower: str) -> str:
    """
    Parse answer text to determine verdict
    
    Handles different question types:
    - Permission questions: "Can X?" → YES = Compliant
    - Requirement questions: "Is X required?" → NO/YES = Compliant
    """
    
    answer = result.get('answer', '').strip()
    if not answer:
        return "⚠️ Unknown"
    
    # Get first 300 chars (where verdict usually appears)
    answer_lower = answer.lower()[:300]
    
    # Detect question type
    is_permission = (
        query_lower.startswith('can ') or
        query_lower.startswith('may ') or
        query_lower.startswith('is it allowed') or
        query_lower.startswith('is it permitted')
    )
    
    is_requirement = (
        'is consent required' in query_lower or
        'is authorization required' in query_lower or
        'is required for' in query_lower or
        'required to' in query_lower or
        'must obtain' in query_lower
    )
    
    # Extract first word/phrase
    first_line = answer_lower.split('\n')[0].strip()
    
    # Remove markdown/formatting
    first_line = first_line.replace('**', '').replace('*', '').strip()
    
    # Get first word
    words = first_line.split()
    first_word = words[0] if words else ""
    
    # ================================================================
    # Permission Questions: "Can X do Y?"
    # ================================================================
    if is_permission:
        # YES = action is allowed = COMPLIANT
        # NO = action not allowed = VIOLATION
        
        if first_word in ['yes', 'yes,', '1.', 'yes.']:
            return "✅ Compliant"
        elif 'yes -' in first_line or 'yes,' in first_line:
            return "✅ Compliant"
        elif first_word in ['no', 'no,', '2.', 'no.']:
            return "❌ Violation"
        elif 'no -' in first_line or 'no,' in first_line:
            return "❌ Violation"
    
    # ================================================================
    # Requirement Questions: "Is X required?"
    # ================================================================
    elif is_requirement:
        # Both YES and NO can be compliant (depends on what's correct)
        # NO = not required = compliant (if that's correct)
        # YES = is required = compliant (if that's correct)
        
        # Look for verdict keywords in answer
        if 'compliant' in answer_lower or 'permitted' in answer_lower:
            return "✅ Compliant"
        elif 'violation' in answer_lower or 'not permitted' in answer_lower:
            return "❌ Violation"
        else:
            # Default: both YES and NO answers are compliant for requirement questions
            # (they're just stating what the requirement is)
            return "✅ Compliant"
    
    # ================================================================
    # General Pattern Matching
    # ================================================================
    
    # Compliant indicators
    if any(phrase in answer_lower for phrase in [
        'compliant', 'is permitted', 'is allowed', 'yes -',
        'yes,', 'this is allowed', 'may use', 'may disclose'
    ]):
        return "✅ Compliant"
    
    # Violation indicators
    if any(phrase in answer_lower for phrase in [
        'violation', 'not permitted', 'not allowed', 'prohibited',
        'no -', 'no,', 'cannot', 'may not'
    ]):
        return "❌ Violation"
    
    # If we can't determine, return unknown
    return "⚠️ Unknown"


def build_comparison_table(results: list, query: str) -> list:
    """
    Build comparison table data from experiment results
    
    Args:
        results: List of experiment result dicts
        query: The original query
        
    Returns:
        List of dicts for display in table
    """
    
    # Map experiment names to display names
    exp_name_map = {
        "Baseline": "Baseline (No Context)",
        "RAG": "RAG (Retrieval-Augmented Generation)",
        "RAG (Retrieval-Augmented Generation)": "RAG (Retrieval-Augmented Generation)",
        "Pipeline4Compliance ⭐": "Two-Tier Pipeline ⭐",
        "Two-Tier Pipeline ⭐": "Two-Tier Pipeline ⭐",
        "Agentic Multi-Agent System ⭐": "Multi-Agent + Two-Tier Verification 🚀",
        "Multi-Agent + Two-Tier Verification 🚀": "Multi-Agent + Two-Tier Verification 🚀"
    }
    
    comparison_data = []
    
    for result in results:
        # Skip error results
        if "error" in result and result.get("error"):
            continue
        
        # Get experiment name
        result_name = result.get('name', 'Unknown')
        exp_name = exp_name_map.get(result_name, result_name)
        
        # Determine verdict
        verdict = determine_verdict_for_comparison(result, query)
        
        # Check if uses retrieval
        uses_retrieval = (
            'retrieved_policies' in result or
            'matched_policies' in result.get('precis_result', {}).get('json_response', {})
        )
        
        # Check if uses Précis
        uses_precis = 'precis_result' in result
        
        # Get duration
        duration = result.get('duration', 0)
        
        # Get steps count
        steps = len(result.get('steps', []))
        
        comparison_data.append({
            "Experiment": exp_name,
            "Verdict": verdict,
            "Duration (s)": f"{duration:.2f}",
            "Steps": steps,
            "Uses Retrieval": "✅" if uses_retrieval else "❌",
            "Uses Précis": "✅" if uses_precis else "❌"
        })
    
    return comparison_data


def display_comparison_analysis(comparison_data: list):
    """
    Display agreement analysis below comparison table
    """
    
    if not comparison_data:
        return
    
    # Count verdicts
    verdicts = [row['Verdict'] for row in comparison_data]
    compliant = sum(1 for v in verdicts if "Compliant" in v)
    violation = sum(1 for v in verdicts if "Violation" in v)
    unknown = sum(1 for v in verdicts if "Unknown" in v)
    total = len(verdicts)
    
    # Determine consensus
    if compliant == total:
        st.success(f"✅ **Perfect Agreement: All {total} experiments say COMPLIANT**")
    elif violation == total:
        st.error(f"❌ **Perfect Agreement: All {total} experiments say VIOLATION**")
    elif compliant > violation and compliant > unknown:
        st.warning(f"⚠️ **Majority: {compliant}/{total} say COMPLIANT** (disagreement: {violation} violation, {unknown} unknown)")
    elif violation > compliant and violation > unknown:
        st.warning(f"⚠️ **Majority: {violation}/{total} say VIOLATION** (disagreement: {compliant} compliant, {unknown} unknown)")
    else:
        st.error(f"⚠️ **No Consensus**: {compliant} compliant, {violation} violation, {unknown} unknown")