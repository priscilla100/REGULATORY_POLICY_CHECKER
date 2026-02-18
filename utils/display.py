"""
FIXED VERDICT DETERMINATION
Properly handles RAG, Baseline, Pipeline, and Agentic results
"""

import streamlit as st
import re
import pandas as pd

def determine_verdict(result: dict, query: str = "") -> dict:
    """
    Extract verdict from any experiment type with query-aware logic
    
    FIXED: Now properly handles RAG results
    """
    
    query_lower = query.lower() if query else ""
    
    # ================================================================
    # PRIORITY 1: Explicit compliance_status (Agentic)
    # ================================================================
    if 'compliance_status' in result:
        status_str = result['compliance_status']
        if "COMPLIANT" in status_str and "NOT" not in status_str and "VIOLATION" not in status_str:
            return {'status': 'compliant', 'text': 'COMPLIANT'}
        elif "VIOLATION" in status_str or "NOT COMPLIANT" in status_str:
            return {'status': 'violation', 'text': 'VIOLATION DETECTED'}
        else:
            return {'status': 'unknown', 'text': 'INCONCLUSIVE'}
    
    # ================================================================
    # PRIORITY 2: Explicit verdict field (RAG, Baseline)
    # ================================================================
    if 'verdict' in result:
        verdict_str = result['verdict'].upper()
        
        if "COMPLIANT" in verdict_str and "NOT" not in verdict_str:
            return {'status': 'compliant', 'text': 'COMPLIANT'}
        elif "VIOLATION" in verdict_str:
            return {'status': 'violation', 'text': 'VIOLATION'}
        elif "UNCLEAR" in verdict_str or "UNKNOWN" in verdict_str:
            # For RAG/Baseline, parse the answer to determine verdict
            return parse_answer_for_verdict(result, query_lower)
        else:
            return parse_answer_for_verdict(result, query_lower)
    
    # ================================================================
    # PRIORITY 3: OCaml Précis result (Pipeline/Agentic)
    # ================================================================
    if 'precis_result' in result:
        return determine_precis_verdict(result, query_lower)
    
    # ================================================================
    # PRIORITY 4: Verified flag (Pipeline)
    # ================================================================
    if 'verified' in result:
        if result['verified']:
            return {'status': 'compliant', 'text': 'COMPLIANT'}
        else:
            return {'status': 'violation', 'text': 'VIOLATION DETECTED'}
    
    # ================================================================
    # PRIORITY 5: Parse answer text (Final fallback)
    # ================================================================
    return parse_answer_for_verdict(result, query_lower)


def parse_answer_for_verdict(result: dict, query_lower: str) -> dict:
    """
    Parse the answer text to determine verdict
    
    This handles RAG and Baseline results that don't have explicit verdicts
    """
    
    answer = result.get('answer', '').lower()
    
    if not answer:
        return {'status': 'unknown', 'text': 'NO ANSWER PROVIDED'}
    
    # Get first 200 characters for analysis (where verdict usually is)
    answer_start = answer[:200]
    
    # Check if this is a requirement question
    is_requirement_q = any(word in query_lower for word in [
        'is consent required', 'is authorization required',
        'must obtain', 'required to', 'is required'
    ])
    
    # Check if this is an action question
    is_action_q = any(word in query_lower for word in [
        'can', 'may', 'allowed to', 'permitted'
    ])
    
    # Pattern matching for answers
    if is_requirement_q:
        # "Is X required?" → "NO" = Compliant, "YES" = Compliant (requirement exists)
        if answer_start.startswith('no') or 'not required' in answer_start:
            return {'status': 'compliant', 'text': 'NOT REQUIRED (Compliant)'}
        elif answer_start.startswith('yes') or 'is required' in answer_start:
            return {'status': 'compliant', 'text': 'REQUIRED (Compliant)'}
    
    elif is_action_q:
        # "Can X do Y?" → "YES" = Compliant, "NO" = Violation
        if answer_start.startswith('yes') or answer_start.startswith('1. direct answer: yes'):
            return {'status': 'compliant', 'text': 'COMPLIANT'}
        elif answer_start.startswith('no') or answer_start.startswith('1. direct answer: no'):
            return {'status': 'violation', 'text': 'VIOLATION'}
    
    # General pattern matching
    compliant_patterns = [
        'compliant', 'permitted', 'allowed', 'authorized',
        'yes, this is allowed', 'this is permitted'
    ]
    
    violation_patterns = [
        'violation', 'not permitted', 'not allowed', 'prohibited',
        'requires authorization', 'no, this is not'
    ]
    
    # Count pattern matches
    compliant_count = sum(1 for p in compliant_patterns if p in answer_start)
    violation_count = sum(1 for p in violation_patterns if p in answer_start)
    
    if compliant_count > violation_count:
        return {'status': 'compliant', 'text': 'COMPLIANT'}
    elif violation_count > compliant_count:
        return {'status': 'violation', 'text': 'VIOLATION'}
    else:
        return {'status': 'unknown', 'text': 'UNCLEAR'}


def determine_precis_verdict(result: dict, query_lower: str) -> dict:
    """
    Determine verdict from OCaml Précis results
    """
    
    precis = result.get('precis_result', {})
    
    if not precis.get('success', False):
        return {'status': 'unknown', 'text': 'VERIFICATION FAILED'}
    
    precis_json = precis.get('json_response', {})
    answer = result.get('answer', '').lower()
    
    # Check if this is a requirement question
    is_requirement_question = any(word in query_lower for word in [
        'is consent required', 'is authorization required',
        'must obtain', 'required to', 'need to have'
    ])
    
    if is_requirement_question:
        # For requirement questions, check the LLM's answer
        if answer.startswith('no') or 'not required' in answer[:100]:
            return {'status': 'compliant', 'text': 'NOT REQUIRED (Compliant)'}
        elif answer.startswith('yes') or 'is required' in answer[:100]:
            return {'status': 'compliant', 'text': 'REQUIRED (Compliant)'}
    
    # Check overall_compliant flag
    if 'overall_compliant' in precis_json:
        if precis_json['overall_compliant']:
            return {'status': 'compliant', 'text': 'COMPLIANT'}
        else:
            violations = precis_json.get('violations', [])
            return {
                'status': 'violation',
                'text': f'VIOLATION DETECTED'
            }
    
    # Fallback: check evaluations
    evaluations = precis_json.get('evaluations', [])
    if evaluations:
        violations = [e for e in evaluations if e.get('evaluation', {}).get('result') == 'false']
        if violations:
            return {'status': 'violation', 'text': 'VIOLATION'}
        else:
            return {'status': 'compliant', 'text': 'COMPLIANT'}
    
    return {'status': 'unknown', 'text': 'NO VERIFICATION DATA'}


def safe_metric_value(value):
    """Convert any value to a safe metric value"""
    if isinstance(value, list):
        return len(value)
    elif isinstance(value, (int, float)):
        return value
    elif isinstance(value, str) and len(value) < 20:
        return value
    elif isinstance(value, str):
        return value[:15]
    else:
        return str(value)[:15]


# ============================================================================
# COMPLETE DISPLAY FUNCTION (ALL TECHNICAL DETAILS IN EXPANDERS)
# ============================================================================

def display_unified_result(result: dict, query: str):
    """
    Complete unified display with ALL technical details in expanders
    """
    
    verdict = determine_verdict(result, query)
    
    # ================================================================
    # USER-FACING SECTION (Always visible)
    # ================================================================
    
    st.markdown("## 📊 Results")
    
    # Question
    st.markdown("### 📋 Question")
    st.info(query)
    
    # Verdict Badge
    st.markdown("### 🎯 Verdict")
    if verdict['status'] == 'compliant':
        st.success(f"## ✅ {verdict['text']}")
    elif verdict['status'] == 'violation':
        st.error(f"## ❌ {verdict['text']}")
    else:
        st.warning(f"## ⚠️ {verdict['text']}")
    
    # Metrics
    st.markdown("### 📊 Metrics")
    display_unified_metrics(result, verdict)
    
    # Main Answer
    st.markdown("### 💬 Explanation")
    answer = result.get('answer', 'No answer provided')
    st.markdown(answer)
    
    # Violation Summary (if any) - Keep visible for important info
    if 'precis_result' in result:
        precis_json = result.get('precis_result', {}).get('json_response', {})
        violations = precis_json.get('violations', [])
        
        if violations and len(violations) > 0:
            st.markdown("### ⚠️ Policy Violations")
            st.error(f"🚨 Found **{len(violations)}** HIPAA Policy Violations")
            
            violation_sections = [v.split('-')[1] if '-' in v else v for v in violations]
            
            if len(violation_sections) <= 5:
                st.markdown("**" + ", ".join([f"§{s}" for s in violation_sections]) + "**")
            else:
                shown = violation_sections[:5]
                remaining = len(violation_sections) - 5
                st.markdown("**" + ", ".join([f"§{s}" for s in shown]) + f" and {remaining} more**")
            
            st.caption("💡 Expand 'Technical Details' below to see full violation explanations")
    
    # ================================================================
    # TECHNICAL SECTION (All in expanders)
    # ================================================================
    
    with st.expander("🔬 Technical Details (for debugging)", expanded=False):
        
        # Processing Steps
        if result.get('steps'):
            st.markdown("#### 🔄 Processing Pipeline")
            for step in result['steps']:
                st.text(f"• {step}")
            st.markdown("---")
        
        # Extracted Facts
        if 'extracted_facts' in result:
            st.markdown("#### 🧩 Extracted Facts")
            st.json(result['extracted_facts'])
            st.markdown("---")
        
        # Formula
        if 'formula' in result:
            st.markdown("#### 📐 Formal Logic Formula")
            st.code(result['formula'], language="text")
            st.markdown("---")
        
        # Retrieved Policies (RAG)
        if 'retrieved_policies' in result:
            retrieved = result['retrieved_policies']
            if isinstance(retrieved, list) and len(retrieved) > 0:
                st.markdown("#### 📚 Retrieved Policies")
                st.info(f"Retrieved {len(retrieved)} policies:")
                for policy_id in retrieved:
                    st.write(f"• {policy_id}")
                st.markdown("---")
        
        # Top Matched Policies
        if 'precis_result' in result:
            precis_json = result.get('precis_result', {}).get('json_response', {})
            matched_policies = precis_json.get('matched_policies', [])
            
            if matched_policies:
                st.markdown("#### 📚 Top Relevant HIPAA Sections")
                top_policies = sorted(matched_policies, 
                                     key=lambda x: x.get('relevance_score', 0), 
                                     reverse=True)[:3]
                
                for i, policy in enumerate(top_policies, 1):
                    st.write(f"{i}. **{policy.get('regulation', 'N/A')} §{policy.get('section', 'N/A')}**")
                    st.caption(policy.get('description', 'No description'))
                
                st.markdown("---")
            
            # Detailed Violations
            evaluations = precis_json.get('evaluations', [])
            violation_details = [e for e in evaluations 
                                if e.get('evaluation', {}).get('result') == 'false']
            
            if violation_details:
                st.markdown("#### ⚠️ Detailed Violation Information")
                for v in violation_details:
                    st.error(f"**{v.get('regulation', 'N/A')} §{v.get('section', 'N/A')}**: "
                            f"{v.get('description', 'No description')}")
                st.markdown("---")
        
        # OCaml Full Output (Most technical - in nested expander)
        if 'precis_result' in result:
            with st.expander("⚙️ OCaml Précis Engine (Full Output)", expanded=False):
                precis = result['precis_result']
                
                if precis.get('success'):
                    st.success("✅ OCaml processing successful")
                    
                    if 'pipeline_steps' in precis:
                        st.markdown("**Pipeline Steps:**")
                        for step in precis['pipeline_steps']:
                            st.text(f"• {step}")
                    
                    st.markdown("**Full OCaml JSON Output:**")
                    st.json(precis.get('json_response', {}))
                else:
                    st.error(f"❌ OCaml Error: {precis.get('error', 'Unknown error')}")
        
        # Full Result JSON (Deepest level - nested expander)
        with st.expander("📄 Full Result JSON (Raw Data)", expanded=False):
            st.json(result)


def display_unified_metrics(result: dict, verdict: dict):
    """Metrics display with safe value handling"""
    
    cols = st.columns(5)
    
    # Duration
    cols[0].metric("⏱️ Duration", f"{result.get('duration', 0):.1f}s")
    
    # Verdict
    if verdict['status'] == 'compliant':
        cols[1].metric("Verdict", "✅ COMPLIANT", delta="Pass")
    elif verdict['status'] == 'violation':
        cols[1].metric("Verdict", "❌ VIOLATION", delta="Fail", delta_color="inverse")
    else:
        cols[1].metric("Verdict", "⚠️ UNKNOWN", delta="Unclear")
    
    # Confidence/Policies
    if 'analysis' in result and 'confidence' in result['analysis']:
        confidence = result['analysis']['confidence'] * 100
        cols[2].metric("🎯 Confidence", f"{confidence:.0f}%")
    elif 'precis_result' in result:
        precis_json = result.get('precis_result', {}).get('json_response', {})
        policies_checked = len(precis_json.get('evaluations', []))
        cols[2].metric("📋 Policies", policies_checked)
    else:
        cols[2].metric("📚 Source", "LLM")
    
    # Retrieved/Compliant
    if 'retrieved_policies' in result:
        retrieved = result.get('retrieved_policies', 0)
        count = safe_metric_value(retrieved)
        cols[3].metric("🔍 Retrieved", count)
    elif 'precis_result' in result:
        precis_json = result.get('precis_result', {}).get('json_response', {})
        evaluations = precis_json.get('evaluations', [])
        compliant = len([e for e in evaluations if e.get('evaluation', {}).get('result') == 'true'])
        cols[3].metric("✅ Compliant", compliant)
    else:
        cols[3].metric("🔄 Steps", len(result.get('steps', [])))
    
    # Violations/Method
    if 'precis_result' in result:
        precis_json = result.get('precis_result', {}).get('json_response', {})
        evaluations = precis_json.get('evaluations', [])
        violations = len([e for e in evaluations if e.get('evaluation', {}).get('result') == 'false'])
        if violations > 0:
            cols[4].metric("❌ Violations", violations, delta_color="inverse")
        else:
            cols[4].metric("❌ Violations", "0")
    else:
        method = result.get('method', 'Unknown')
        cols[4].metric("🛠️ Method", method[:12])


def determine_verdict_for_comparison(result: dict, query: str = "") -> str:
    """
    Determine verdict for comparison table display
    
    Returns: "✅ Compliant", "❌ Violation", or "⚠️ Unknown"
    """
    
    query_lower = query.lower() if query else ""
    
    # Check 1: Explicit compliance_status
    if 'compliance_status' in result:
        status = result['compliance_status']
        if "COMPLIANT" in status and "VIOLATION" not in status:
            return "✅ Compliant"
        elif "VIOLATION" in status:
            return "❌ Violation"
        else:
            return "⚠️ Unknown"
    
    # Check 2: Explicit verdict field (RAG, Baseline)
    if 'verdict' in result:
        verdict = result['verdict'].upper()
        
        # Handle verdict strings
        if "✅" in verdict or "COMPLIANT" in verdict:
            # But double-check by parsing answer
            answer = result.get('answer', '').lower()
            if answer and len(answer) > 10:
                # For action questions: "YES" = Compliant
                if query_lower.startswith('can ') or query_lower.startswith('may '):
                    if answer.startswith('yes') or answer.startswith('1. direct answer: yes'):
                        return "✅ Compliant"
                    elif answer.startswith('no'):
                        return "❌ Violation"
            return "✅ Compliant"
        
        elif "❌" in verdict or "VIOLATION" in verdict:
            return "❌ Violation"
        
        elif "⚠️" in verdict or "UNCLEAR" in verdict or "UNKNOWN" in verdict:
            # Parse answer to determine
            return parse_answer_verdict(result, query_lower)
        
        else:
            return parse_answer_verdict(result, query_lower)
    
    # Check 3: OCaml Précis result
    if 'precis_result' in result:
        return determine_precis_verdict_for_comparison(result, query_lower)
    
    # Check 4: Verified flag
    if 'verified' in result:
        return "✅ Compliant" if result['verified'] else "❌ Violation"
    
    # Check 5: Parse answer
    return parse_answer_verdict(result, query_lower)


def parse_answer_verdict(result: dict, query_lower: str) -> str:
    """Parse answer text to determine verdict"""
    
    answer = result.get('answer', '').lower()
    if not answer or len(answer) < 10:
        return "⚠️ Unknown"
    
    answer_start = answer[:200]
    
    # Action questions: "Can X do Y?"
    if any(word in query_lower for word in ['can ', 'may ', 'allowed to']):
        if answer_start.startswith('yes') or 'yes,' in answer_start[:20]:
            return "✅ Compliant"
        elif answer_start.startswith('no'):
            return "❌ Violation"
    
    # Requirement questions: "Is X required?"
    if any(word in query_lower for word in ['is required', 'must ', 'need to']):
        # Both YES and NO can be compliant
        if answer_start.startswith('yes') or answer_start.startswith('no'):
            return "✅ Compliant"
    
    # Pattern matching
    if 'compliant' in answer_start or 'permitted' in answer_start:
        return "✅ Compliant"
    elif 'violation' in answer_start or 'not permitted' in answer_start:
        return "❌ Violation"
    
    return "⚠️ Unknown"


def determine_precis_verdict_for_comparison(result: dict, query_lower: str) -> str:
    """Determine verdict from OCaml Précis with false positive filtering"""
    
    precis = result.get('precis_result', {})
    
    if not precis.get('success'):
        return "⚠️ Unknown"
    
    precis_json = precis.get('json_response', {})
    
    # Get evaluations
    evaluations = precis_json.get('evaluations', [])
    if not evaluations:
        return "⚠️ Unknown"
    
    # Filter out false positive violations
    real_violations = []
    false_positives = []
    
    for eval in evaluations:
        if eval.get('evaluation', {}).get('result') == 'false':
            policy_id = eval.get('policy_id', '')
            description = eval.get('description', '').lower()
            
            # These are PROCEDURAL/ORGANIZATIONAL requirements, not substantive violations
            false_positive_patterns = [
                'minimum necessary',           # Procedural - about HOW MUCH, not WHETHER
                'privacy officer',             # Organizational
                'security officer',            # Organizational
                'policies and procedures',     # Organizational
                'safeguards',                  # Organizational
                'training',                    # Organizational
                'documentation',               # Organizational
                'retention',                   # Organizational
                'evaluation',                  # Organizational
                'complaint process',           # Organizational
                'sanctions',                   # Organizational
                'mitigation',                  # Organizational
                'incident response'            # Organizational
            ]
            
            if any(pattern in description for pattern in false_positive_patterns):
                false_positives.append(eval)
            else:
                real_violations.append(eval)
    
    # Only count REAL violations
    if len(real_violations) > 0:
        return "❌ Violation"
    else:
        return "✅ Compliant"


# ============================================================================
# FIX 2: UPDATED COMPARISON DISPLAY
# ============================================================================

def display_comparison(results: dict, query: str):
    """
    Fixed comparison table with proper verdict determination
    """
    
    st.markdown("## 📈 Comparison")
    
    # Build comparison data
    comparison_data = []
    
    for name, result in results.items():
        # Use FIXED verdict determination
        verdict = determine_verdict_for_comparison(result, query)
        
        comparison_data.append({
            "Experiment": name,
            "Verdict": verdict,
            "Duration (s)": f"{result.get('duration', 0):.2f}",
            "Steps": len(result.get('steps', [])),
            "Uses Retrieval": "✅" if 'retrieved_policies' in result else "❌",
            "Uses Précis": "✅" if 'precis_result' in result else "❌"
        })
    
    # Display table
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Agreement analysis
    verdicts = [row['Verdict'] for row in comparison_data]
    compliant_count = sum(1 for v in verdicts if "Compliant" in v)
    violation_count = sum(1 for v in verdicts if "Violation" in v)
    unknown_count = sum(1 for v in verdicts if "Unknown" in v)
    
    # Show agreement status
    if compliant_count == len(verdicts):
        st.success(f"✅ **All {len(verdicts)} experiments agree: COMPLIANT**")
    elif violation_count == len(verdicts):
        st.error(f"❌ **All {len(verdicts)} experiments agree: VIOLATION**")
    elif compliant_count > violation_count:
        st.warning(f"⚠️ **Majority ({compliant_count}/{len(verdicts)}) say: COMPLIANT**")
        st.caption(f"Disagreement: {violation_count} say violation, {unknown_count} unclear")
    elif violation_count > compliant_count:
        st.warning(f"⚠️ **Majority ({violation_count}/{len(verdicts)}) say: VIOLATION**")
        st.caption(f"Disagreement: {compliant_count} say compliant, {unknown_count} unclear")
    else:
        st.error(f"⚠️ **No consensus** - {compliant_count} compliant, {violation_count} violation, {unknown_count} unclear")


def determine_verdict_for_comparison(result: dict, query: str = "") -> str:
    """
    Comprehensive verdict determination with query context
    
    Priority:
    1. Explicit compliance_status field
    2. Verification tier + compliant field
    3. verified field
    4. Parse answer text
    """
    
    # Priority 1: Check compliance_status (most reliable)
    if 'compliance_status' in result:
        status = str(result['compliance_status']).upper()
        if "COMPLIANT" in status and "VIOLATION" not in status:
            return "✅ Compliant"
        elif "VIOLATION" in status:
            return "❌ Violation"
    
    # Priority 2: Check compliant field (two-tier systems)
    if 'compliant' in result:
        if result['compliant'] is True:
            return "✅ Compliant"
        elif result['compliant'] is False:
            # Double-check: OCaml failure shouldn't default to violation
            if 'formal_result' in result:
                formal = result['formal_result']
                if not formal.get('success', False):
                    # OCaml failed - check if we have procedural exception
                    if result.get('procedural_exception'):
                        return "✅ Compliant"
                    # Otherwise uncertain
                    return "⚠️ Unknown (OCaml Failed)"
            return "❌ Violation"
    
    # Priority 3: Check verified field (legacy)
    if 'verified' in result:
        return "✅ Compliant" if result['verified'] else "❌ Violation"
    
    # Priority 4: Parse answer text
    answer = result.get('answer', '').lower().strip()
    if not answer:
        return "⚠️ Unknown"
    
    # Check if this is a permission question
    query_lower = query.lower().strip()
    is_permission_q = (
        query_lower.startswith('can ') or
        query_lower.startswith('may ') or
        query_lower.startswith('is it allowed')
    )
    
    is_requirement_q = (
        'is consent required' in query_lower or
        'is authorization required' in query_lower or
        'is required' in query_lower
    )
    
    # Extract first word of answer
    first_word = answer.split()[0] if answer.split() else ""
    
    if is_permission_q:
        # "Can X do Y?" → YES = Compliant, NO = Violation
        if first_word in ['yes', '**yes**', '1.', 'yes,']:
            return "✅ Compliant"
        elif first_word in ['no', '**no**', '2.']:
            return "❌ Violation"
    
    elif is_requirement_q:
        # "Is consent required?" → NO = Compliant (consent NOT required)
        # This is TRICKY - the answer and verdict are different!
        if first_word in ['no', '**no**']:
            # "NO consent required" → COMPLIANT
            return "✅ Compliant"
        elif first_word in ['yes', '**yes**']:
            # "YES consent required" → depends on context
            # (might be explaining WHEN it's required)
            return "⚠️ Unclear"
    
    # Default: look for compliance indicators in full answer
    if 'compliant' in answer or 'permitted' in answer or 'allowed' in answer:
        return "✅ Compliant"
    elif 'violation' in answer or 'not permitted' in answer or 'prohibited' in answer:
        return "❌ Violation"
    
    return "⚠️ Unknown"