"""
Comparison Table Utilities

Fixed verdict determination for all experiment types:
- Baseline (LLM only)
- RAG (Retrieval + LLM)  
- Pipeline (Two-Tier)
- Multi-Agent (Two-Tier)

Handles:
- Permission questions: "Can X?" → YES = Compliant
- Requirement questions: "Is X required?" → Both YES/NO can be compliant
- OCaml failures
- Missing fields
"""

from typing import Dict, List


def determine_verdict_for_comparison(result: dict, query: str = "") -> str:
    """
    COMPLETE FIX for comparison table verdicts
    
    Returns:
        "✅ Compliant", "❌ Violation", or "⚠️ Unknown"
    
    Handles ALL experiment types and edge cases
    """
    
    query_lower = query.lower().strip() if query else ""
    
    # ================================================================
    # PRIORITY 1: Check compliance_status (Two-Tier systems)
    # ================================================================
    if 'compliance_status' in result:
        status = str(result['compliance_status']).upper()
        
        # Check for emoji or text indicators
        if "✅" in status or ("COMPLIANT" in status and "VIOLATION" not in status and "NOT" not in status):
            return "✅ Compliant"
        elif "❌" in status or "VIOLATION" in status or "NOT COMPLIANT" in status:
            return "❌ Violation"
        elif "⚠️" in status or "UNKNOWN" in status or "UNCLEAR" in status:
            return "⚠️ Unknown"
    
    # ================================================================
    # PRIORITY 2: Check compliant field (Two-Tier systems)
    # ================================================================
    if 'compliant' in result:
        compliant = result['compliant']
        
        if compliant is True:
            return "✅ Compliant"
        
        elif compliant is False:
            # CRITICAL: Check if OCaml failed (don't trust false negatives)
            formal_result = result.get('formal_result', {})
            
            if formal_result:
                # Check if OCaml execution actually failed
                if not formal_result.get('success', False):
                    # OCaml failed - check if procedural exception applied
                    if result.get('procedural_exception'):
                        return "✅ Compliant"
                    
                    # OCaml failed, no exception - uncertain
                    return "⚠️ Unknown"
            
            # compliant=False with successful OCaml - real violation
            return "❌ Violation"
    
    # ================================================================
    # PRIORITY 3: Check verdict field (RAG, Baseline)
    # ================================================================
    if 'verdict' in result:
        verdict = str(result['verdict']).upper()
        
        if "✅" in verdict or "COMPLIANT" in verdict:
            return "✅ Compliant"
        elif "❌" in verdict or "VIOLATION" in verdict:
            return "❌ Violation"
        elif "⚠️" in verdict or "UNCLEAR" in verdict or "UNKNOWN" in verdict:
            # Try parsing answer
            return parse_answer_verdict(result, query_lower)
        else:
            # Verdict field exists but unclear - parse answer
            return parse_answer_verdict(result, query_lower)
    
    # ================================================================
    # PRIORITY 4: Check verified field (legacy)
    # ================================================================
    if 'verified' in result:
        return "✅ Compliant" if result['verified'] else "❌ Violation"
    
    # ================================================================
    # PRIORITY 5: Parse answer text (final fallback)
    # ================================================================
    return parse_answer_verdict(result, query_lower)


def parse_answer_verdict(result: dict, query_lower: str) -> str:
    """
    Parse answer text to determine verdict
    
    Handles different question types:
    - Permission: "Can X?" → YES = Compliant, NO = Violation
    - Requirement: "Is X required?" → Both YES/NO can be compliant
    
    Returns:
        "✅ Compliant", "❌ Violation", or "⚠️ Unknown"
    """
    
    answer = result.get('answer', '').strip()
    if not answer:
        return "⚠️ Unknown"
    
    # Get first 300 chars (where verdict usually appears)
    answer_lower = answer.lower()[:300]
    
    # Clean markdown formatting
    first_line = answer_lower.split('\n')[0].strip()
    first_line = first_line.replace('**', '').replace('*', '').strip()
    
    # Get first word
    words = first_line.split()
    first_word = words[0] if words else ""
    
    # ================================================================
    # DETECT QUESTION TYPE
    # ================================================================
    
    is_permission = (
        query_lower.startswith('can ') or
        query_lower.startswith('may ') or
        query_lower.startswith('is it allowed') or
        query_lower.startswith('is it permitted') or
        'can ' in query_lower[:20] or  # "Can X do Y?"
        'may ' in query_lower[:20]
    )
    
    is_requirement = (
        'is consent required' in query_lower or
        'is authorization required' in query_lower or
        'is required for' in query_lower or
        'required to' in query_lower or
        'must obtain' in query_lower or
        'need consent' in query_lower or
        'need authorization' in query_lower
    )
    
    # ================================================================
    # PERMISSION QUESTIONS: "Can X do Y?"
    # ================================================================
    
    if is_permission:
        # YES = action is allowed = COMPLIANT
        # NO = action not allowed = VIOLATION
        
        yes_indicators = ['yes', 'yes,', 'yes.', '1.', 'yes -', 'yes –']
        no_indicators = ['no', 'no,', 'no.', '2.', 'no -', 'no –']
        
        # Check first word
        if first_word in yes_indicators:
            return "✅ Compliant"
        elif first_word in no_indicators:
            return "❌ Violation"
        
        # Check first line
        if any(ind in first_line for ind in yes_indicators):
            return "✅ Compliant"
        elif any(ind in first_line for ind in no_indicators):
            return "❌ Violation"
    
    # ================================================================
    # REQUIREMENT QUESTIONS: "Is X required?"
    # ================================================================
    
    elif is_requirement:
        # Both YES and NO can be compliant
        # (They're just stating what the requirement is)
        
        # Look for compliance/violation keywords in answer
        if any(phrase in answer_lower for phrase in [
            'compliant', 'permitted', 'is allowed', 'may use', 'may disclose'
        ]):
            return "✅ Compliant"
        
        elif any(phrase in answer_lower for phrase in [
            'violation', 'not permitted', 'not allowed', 'prohibited'
        ]):
            return "❌ Violation"
        
        else:
            # Default: requirement questions are about the rule itself
            # Both YES and NO answers are "compliant" (correctly stating the rule)
            return "✅ Compliant"
    
    # ================================================================
    # GENERAL PATTERN MATCHING
    # ================================================================
    
    # Compliant indicators
    compliant_patterns = [
        'compliant', 'is permitted', 'is allowed', 'yes -', 'yes,',
        'this is allowed', 'may use', 'may disclose', 'permitted to'
    ]
    
    # Violation indicators  
    violation_patterns = [
        'violation', 'not permitted', 'not allowed', 'prohibited',
        'no -', 'no,', 'cannot', 'may not', 'not compliant'
    ]
    
    # Count matches
    compliant_count = sum(1 for p in compliant_patterns if p in answer_lower)
    violation_count = sum(1 for p in violation_patterns if p in answer_lower)
    
    if compliant_count > violation_count:
        return "✅ Compliant"
    elif violation_count > compliant_count:
        return "❌ Violation"
    
    # ================================================================
    # UNABLE TO DETERMINE
    # ================================================================
    
    return "⚠️ Unknown"


def build_comparison_table(results: list, query: str) -> list:
    """
    Build comparison table data from experiment results
    
    Args:
        results: List of experiment result dicts
        query: The original query
        
    Returns:
        List of dicts suitable for display in table
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
        
        # Skip if no name
        if 'name' not in result:
            continue
        
        # Get experiment name
        result_name = result.get('name', 'Unknown')
        exp_name = exp_name_map.get(result_name, result_name)
        
        # Determine verdict using fixed logic
        verdict = determine_verdict_for_comparison(result, query)
        
        # Check if uses retrieval
        uses_retrieval = (
            'retrieved_policies' in result or
            'matched_policies' in result.get('precis_result', {}).get('json_response', {}) or
            'top_policies' in result
        )
        
        # Check if uses Précis
        uses_precis = 'precis_result' in result or 'formal_result' in result
        
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


def display_comparison_analysis(comparison_data: list) -> str:
    """
    Generate agreement analysis text
    
    Args:
        comparison_data: List of comparison row dicts
        
    Returns:
        Analysis text for display
    """
    
    if not comparison_data:
        return "No valid results to analyze"
    
    # Count verdicts
    verdicts = [row['Verdict'] for row in comparison_data]
    compliant = sum(1 for v in verdicts if "Compliant" in v)
    violation = sum(1 for v in verdicts if "Violation" in v)
    unknown = sum(1 for v in verdicts if "Unknown" in v)
    total = len(verdicts)
    
    # Generate analysis
    if compliant == total:
        return f"✅ **Perfect Agreement: All {total} experiments say COMPLIANT**"
    
    elif violation == total:
        return f"❌ **Perfect Agreement: All {total} experiments say VIOLATION**"
    
    elif compliant > violation and compliant > unknown:
        return (
            f"⚠️ **Majority: {compliant}/{total} say COMPLIANT**\n\n"
            f"Disagreement: {violation} violation, {unknown} unknown"
        )
    
    elif violation > compliant and violation > unknown:
        return (
            f"⚠️ **Majority: {violation}/{total} say VIOLATION**\n\n"
            f"Disagreement: {compliant} compliant, {unknown} unknown"
        )
    
    else:
        return (
            f"⚠️ **No Consensus**\n\n"
            f"{compliant} compliant, {violation} violation, {unknown} unknown"
        )


# Streamlit integration helper
def display_comparison_table_st(results: list, query: str, st):
    """
    Display comparison table in Streamlit
    
    Args:
        results: List of experiment results
        query: Original query
        st: Streamlit module
    """
    
    import pandas as pd
    
    st.markdown("---")
    st.markdown("## 📈 Comparison")
    
    # Build comparison data
    comparison_data = build_comparison_table(results, query)
    
    if not comparison_data:
        st.warning("No valid results to compare")
        return
    
    # Display table
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display analysis
    analysis = display_comparison_analysis(comparison_data)
    
    if "Perfect Agreement" in analysis and "COMPLIANT" in analysis:
        st.success(analysis)
    elif "Perfect Agreement" in analysis and "VIOLATION" in analysis:
        st.error(analysis)
    else:
        st.warning(analysis)
