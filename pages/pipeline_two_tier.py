"""
Updated Pipeline Implementation with Two-Tier Verification

Flow:
1. LLM1: Extract facts from query
2. LLM1: Translate to formal logic
3. TWO-TIER VERIFICATION:
   - Check procedural exceptions first
   - Fall back to OCaml Précis if needed
4. LLM2: Generate explanation

This eliminates false negatives while maintaining formal rigor.
"""

import re
import json
import time
import subprocess
from typing import List, Dict, Tuple, Optional
from anthropic import Anthropic
import os
from config import get_precis_path, ARITY_MAP
from utils.two_tier_verification import (
    TwoTierVerificationWrapper, 
    VerificationResult,
    VerificationTier
)

# Find Précis executable
PRECIS_PATH = get_precis_path()

def validate_fact_structure(fact: List) -> Tuple[bool, str]:
    """Validate fact has correct structure and arity"""
    if not isinstance(fact, list) or len(fact) < 2:
        return False, "Fact must be [predicate, arg1, ...]"
    
    pred = fact[0]
    args = fact[1:]
    
    if pred not in ARITY_MAP:
        return False, f"Unknown predicate: {pred}"
    
    expected = ARITY_MAP[pred]
    if len(args) != expected:
        return False, f"{pred} expects {expected} args, got {len(args)}"
    
    return True, "Valid"


def validate_facts(facts: List[List]) -> Tuple[List[List], List[str]]:
    """
    Validate all facts and return valid ones with warnings
    
    Returns:
        (valid_facts, warnings)
    """
    valid_facts = []
    warnings = []
    
    for fact in facts:
        is_valid, msg = validate_fact_structure(fact)
        if is_valid:
            valid_facts.append(fact)
        else:
            warnings.append(f"⚠️ Skipping invalid fact: {fact} ({msg})")
    
    if not valid_facts:
        # Fallback to minimal facts
        warnings.append("⚠️ No valid facts extracted, using minimal fallback")
        valid_facts = [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]
    
    return valid_facts, warnings


def validate_and_fix_formula(formula: str) -> Tuple[str, List[str], List[str]]:
    """
    Validate formula and attempt auto-fixes
    
    Returns:
        (fixed_formula, warnings, unbound_variables)
    """
    warnings = []
    
    # Remove markdown formatting
    if "```" in formula:
        match = re.search(r'```.*?\n(.*?)\n```', formula, re.DOTALL)
        if match:
            formula = match.group(1).strip()
            warnings.append("🔧 Removed markdown formatting from formula")
    
    # Take only first line if multi-line
    formula_lines = formula.split('\n')
    if len(formula_lines) > 1:
        formula = formula_lines[0].strip()
        warnings.append("🔧 Using only first line of formula")
    
    # Check for unbound variables
    unbound_vars = []
    
    if formula.startswith('forall'):
        # Extract quantified variables
        match = re.search(r'forall\s+([\w,\s]+)\.', formula)
        if match:
            quantified_vars = {v.strip() for v in match.group(1).split(',')}
            
            # Extract all variables used in formula
            var_pattern = r'\b([a-z][a-z0-9_]*)\b'
            used_vars = set(re.findall(var_pattern, formula))
            
            # Exclude keywords
            keywords = {'forall', 'implies', 'and', 'or', 'not', 'true', 'false'}
            used_vars = used_vars - keywords
            
            # Find unbound
            unbound_vars = list(used_vars - quantified_vars)
            
            if unbound_vars:
                warnings.append(f"⚠️ Unbound variables detected: {unbound_vars}")
    
    return formula, warnings, unbound_vars


# ============================================================================
# OCAML PRÉCIS WRAPPER
# ============================================================================

class OCamlPrecisVerifier:
    """
    Wrapper for calling OCaml Précis verification engine
    """
    
    def __init__(self, precis_path: Optional[str] = None):
        self.precis_path = precis_path or PRECIS_PATH
    
    def verify(self, formula: str, facts: List[List]) -> Dict:
        """
        Call OCaml Précis to verify formula against facts
        
        Returns:
            Dictionary with verification results
        """
        
        if self.precis_path is None:
            return {
                "success": False,
                "verified": False,
                "error": "Précis executable not found",
                "output": "",
                "evaluations": [],
                "violations": []
            }
        
        try:
            # Prepare facts for OCaml
            facts_for_ocaml = [
                {"predicate": f[0], "arguments": f[1:]}
                for f in facts if len(f) >= 2
            ]
            
            # Wrap formula in policy structure
            wrapped_formula = f"""regulation HIPAA version "1.0"
policy starts
{formula}
;
policy ends"""
            
            # Build request
            request = {
                "formula": wrapped_formula,
                "facts": {"facts": facts_for_ocaml},
                "regulation": "HIPAA"
            }
            
            # Call OCaml
            proc = subprocess.Popen(
                [self.precis_path, "json"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(self.precis_path) if os.path.dirname(self.precis_path) else "."
            )
            
            output, error = proc.communicate(
                input=json.dumps(request),
                timeout=30
            )
            
            if proc.returncode == 0 and output.strip():
                result = json.loads(output)
                
                # Extract verification status
                evaluations = result.get("evaluations", [])
                violations = result.get("violations", [])
                
                if evaluations:
                    verified = all(
                        e.get("evaluation", {}).get("result") == "true"
                        for e in evaluations
                    )
                else:
                    verified = len(violations) == 0
                
                return {
                    "success": True,
                    "verified": verified,
                    "output": json.dumps(result, indent=2),
                    "error": "",
                    "evaluations": evaluations,
                    "violations": violations,
                    "json_response": result
                }
            else:
                return {
                    "success": False,
                    "verified": False,
                    "output": output,
                    "error": error,
                    "evaluations": [],
                    "violations": []
                }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "verified": False,
                "output": "",
                "error": "Timeout (30s)",
                "evaluations": [],
                "violations": []
            }
        except Exception as e:
            return {
                "success": False,
                "verified": False,
                "output": "",
                "error": str(e),
                "evaluations": [],
                "violations": []
            }


# ============================================================================
# FACT EXTRACTION WITH LLM
# ============================================================================

def extract_facts_with_llm(query: str, client: Anthropic) -> Tuple[List[List], List[str]]:
    """
    Extract facts from natural language query using LLM
    
    Returns:
        (facts, warnings)
    """
    
    extract_prompt = f"""You are a HIPAA compliance expert. Extract ALL relevant entities and facts from this question.

Question: {query}

CRITICAL: Extract facts that describe the ACTUAL SCENARIO, not hypothetical rules.

AVAILABLE PREDICATES (use EXACT arity):

1. Entity types (1 arg):
   - coveredEntity(Entity) - hospitals, clinics, providers, pharmacies
   - protectedHealthInfo(Entity) - medical records, x-rays, lab results, prescriptions
   - publicHealthAuthority(Entity) - CDC, health departments

2. Actions (4 args):
   - disclose(From, To, PHI, Purpose) - ALWAYS 4 args!
   - permittedUseOrDisclosure(From, To, PHI, Purpose) - ONLY if explicitly stated as permitted

3. Authorization (3 args):
   - hasAuthorization(CoveredEntity, Recipient, PHI) - ONLY if authorization mentioned

4. Requirements (1 arg):
   - requiredByLaw(Purpose) - ONLY if explicitly required by law

5. Purpose constants (use as CONSTANTS with @):
   - @Treatment, @Payment, @HealthcareOperations
   - @Research, @PublicHealth, @Emergency

CRITICAL RULES:
- ALWAYS include disclose() fact for action questions
- Include permittedUseOrDisclosure ONLY if the scenario explicitly states it's permitted
- Include hasAuthorization ONLY if authorization is explicitly mentioned
- Use concrete entity names (Hospital1, Pharmacy1, FamilyMember1, etc.)
- Purpose is ALWAYS the 4th argument in disclose()

EXAMPLES:

Q: "Can a hospital share patient records with a specialist for treatment?"
Facts:
[
    ["coveredEntity", "Hospital1"],
    ["protectedHealthInfo", "MedicalRecord1"],
    ["disclose", "Hospital1", "Specialist1", "MedicalRecord1", "@Treatment"]
]

Q: "Can my family pick up prescriptions for me?"
Facts:
[
    ["coveredEntity", "Pharmacy1"],
    ["protectedHealthInfo", "Prescription1"],
    ["disclose", "Pharmacy1", "FamilyMember1", "Prescription1", "@Treatment"]
]

Q: "Can a clinic share lab results with researchers if the patient authorized it?"
Facts:
[
    ["coveredEntity", "Clinic1"],
    ["protectedHealthInfo", "LabResult1"],
    ["disclose", "Clinic1", "Researcher1", "LabResult1", "@Research"],
    ["hasAuthorization", "Clinic1", "Researcher1", "LabResult1"]
]

Now extract from: {query}

Output ONLY valid JSON:
{{
    "entities": ["entity1", "entity2", ...],
    "facts": [
        ["predicate", "arg1", "arg2", ...],
        ...
    ]
}}
"""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{"role": "user", "content": extract_prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in LLM response")
        
        facts_json = json.loads(json_match.group())
        extracted_facts = facts_json.get("facts", [])
        
        # Validate facts
        return validate_facts(extracted_facts)
        
    except Exception as e:
        warnings = [f"❌ Fact extraction failed: {e}"]
        fallback_facts = [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]
        return fallback_facts, warnings


# ============================================================================
# FORMULA TRANSLATION WITH LLM
# ============================================================================

def translate_to_formula_with_llm(query: str, facts: List[List], 
                                  client: Anthropic) -> Tuple[str, List[str]]:
    """
    Translate query to first-order logic formula
    
    Returns:
        (formula, warnings)
    """
    
    translate_prompt = f"""You are translating a compliance question into first-order logic.

Question: {query}
Extracted Facts: {facts}

CRITICAL RULES:
1. Start with "forall" listing ALL variables used in formula
2. Use ONLY these predicates with EXACT arity:
   - coveredEntity(X) [1 arg]
   - protectedHealthInfo(X) [1 arg]
   - publicHealthAuthority(X) [1 arg]
   - hasAuthorization(X,Y,Z) [3 args]
   - requiredByLaw(X) [1 arg]
   - disclose(W,X,Y,Z) [4 args]
   - permittedUseOrDisclosure(W,X,Y,Z) [4 args]

3. DO NOT use purposeIsPurpose or equality checks
4. ALL variables in formula MUST be in forall clause

USE THIS EXACT TEMPLATE:
forall ce, recipient, phi, purpose.
  (coveredEntity(ce)
   and protectedHealthInfo(phi)
   and disclose(ce, recipient, phi, purpose))
  implies
  (permittedUseOrDisclosure(ce, recipient, phi, purpose)
   or hasAuthorization(ce, recipient, phi)
   or requiredByLaw(purpose))

Output ONLY the formula on one line, no explanation:"""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": translate_prompt}]
        )
        
        formula = message.content[0].text.strip()
        
        # Clean up formula
        if "```" in formula:
            match = re.search(r'```.*?\n(.*?)\n```', formula, re.DOTALL)
            if match:
                formula = match.group(1).strip()
        
        formula = formula.split('\n')[0].strip()
        
        # Validate and fix
        fixed_formula, warnings, unbound_vars = validate_and_fix_formula(formula)
        
        # If unbound variables, ask LLM to fix
        if unbound_vars:
            warnings.append(f"🔧 Fixing unbound variables: {unbound_vars}")
            
            fix_prompt = f"""This formula has unbound variables: {unbound_vars}

Formula: {fixed_formula}

Add ALL missing variables to the forall clause.

Output ONLY the corrected formula:"""
            
            fix_message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": fix_prompt}]
            )
            fixed_formula = fix_message.content[0].text.strip()
            warnings.append("✅ Formula fixed")
        
        return fixed_formula, warnings
        
    except Exception as e:
        warnings = [f"❌ Formula translation failed: {e}"]
        # Fallback to standard template
        fallback_formula = (
            "forall ce, recipient, phi, purpose. "
            "(coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) "
            "implies "
            "(permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))"
        )
        return fallback_formula, warnings


# ============================================================================
# EXPLANATION GENERATION WITH LLM
# ============================================================================

def generate_explanation_with_llm(query: str, facts: List[List], 
                                  verification_result: VerificationResult,
                                  client: Anthropic) -> str:
    """
    Generate user-friendly explanation of verification result
    """
    
    if verification_result.tier == VerificationTier.PROCEDURAL_EXCEPTION:
        # Procedural exception - explain why it's allowed
        explain_prompt = f"""Explain this HIPAA compliance result to a non-technical user.

Question: {query}
Result: COMPLIANT (Procedural Exception)
Exception: {verification_result.procedural_exception.name}
Policy: {verification_result.procedural_exception.policy_cite}
Reason: {verification_result.procedural_exception.description}

Provide:
1. Clear YES answer
2. Brief explanation (2-3 sentences) citing the procedural exception
3. Policy citation
4. Practical guidance if helpful

Be clear and reassuring."""
    else:
        # Formal verification result
        explain_prompt = f"""Explain this HIPAA compliance verification to a non-technical user.

Question: {query}
Facts: {json.dumps(facts)}
Result: {"COMPLIANT" if verification_result.compliant else "NON-COMPLIANT"}
Explanation: {verification_result.explanation}

Provide:
1. Direct YES or NO answer
2. Brief explanation (2-3 sentences)
3. Cite HIPAA section if available
4. Actionable guidance if needed

Be clear and concise."""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=600,
            messages=[{"role": "user", "content": explain_prompt}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Unable to generate explanation: {e}"


# ============================================================================
# MAIN PIPELINE WITH TWO-TIER VERIFICATION
# ============================================================================

def pipeline_with_two_tier_verification(query: str, client: Anthropic) -> Dict:
    """
    Complete pipeline with two-tier verification
    
    Flow:
    1. LLM1: Extract facts
    2. LLM1: Translate to formula
    3. Two-Tier Verification (procedural → formal)
    4. LLM2: Generate explanation
    
    Returns:
        Complete result dictionary
    """
    
    start = time.time()
    steps = []
    
    try:
        # ===================================================================
        # STEP 1: FACT EXTRACTION
        # ===================================================================
        
        steps.append("🔍 STEP 1: Extracting facts from query...")
        
        facts, fact_warnings = extract_facts_with_llm(query, client)
        steps.extend(fact_warnings)
        steps.append(f"✅ Extracted {len(facts)} facts:")
        for fact in facts:
            steps.append(f"   • {fact}")
        
        # ===================================================================
        # STEP 2: FORMULA TRANSLATION
        # ===================================================================
        
        steps.append("")
        steps.append("📐 STEP 2: Translating to formal logic...")
        
        formula, formula_warnings = translate_to_formula_with_llm(query, facts, client)
        steps.extend(formula_warnings)
        steps.append(f"✅ Formula: {formula[:100]}...")
        
        # ===================================================================
        # STEP 3: TWO-TIER VERIFICATION (THE KEY INNOVATION!)
        # ===================================================================
        
        steps.append("")
        steps.append("⚙️ STEP 3: Two-Tier Verification System...")
        
        # Create OCaml verifier
        ocaml_verifier = OCamlPrecisVerifier(PRECIS_PATH)
        
        # Create two-tier wrapper
        two_tier_verifier = TwoTierVerificationWrapper(ocaml_verifier)
        
        # Run verification
        verification_result = two_tier_verifier.verify(query, facts, formula)
        
        # Log results
        if verification_result.tier == VerificationTier.PROCEDURAL_EXCEPTION:
            steps.append(f"✅ Tier 1: Procedural Exception Applies")
            steps.append(f"   Exception: {verification_result.procedural_exception.name}")
            steps.append(f"   Policy: {verification_result.procedural_exception.policy_cite}")
            steps.append(f"   Confidence: {verification_result.confidence:.2%}")
            steps.append("   → No formal verification needed!")
        else:
            steps.append("   Tier 1: No procedural exception found")
            steps.append("   → Proceeding to Tier 2: Formal Verification")
            
            if verification_result.formal_result:
                if verification_result.formal_result.get('success'):
                    steps.append("✅ Tier 2: OCaml Précis verification complete")
                    steps.append(f"   Result: {'COMPLIANT' if verification_result.compliant else 'NON-COMPLIANT'}")
                else:
                    steps.append(f"❌ Tier 2: OCaml verification failed")
                    steps.append(f"   Error: {verification_result.formal_result.get('error', 'Unknown')}")
        
        if verification_result.warnings:
            for warning in verification_result.warnings:
                steps.append(f"⚠️ {warning}")
        
        # ===================================================================
        # STEP 4: EXPLANATION GENERATION
        # ===================================================================
        
        steps.append("")
        steps.append("💬 STEP 4: Generating explanation...")
        
        explanation = generate_explanation_with_llm(query, facts, verification_result, client)
        steps.append("✅ Explanation generated")
        
        # ===================================================================
        # FINAL RESULT
        # ===================================================================
        
        compliance_status = "✅ COMPLIANT" if verification_result.compliant else "❌ VIOLATION"
        
        return {
            "name": "Two-Tier Pipeline ⭐",
            "answer": explanation,
            "duration": time.time() - start,
            "steps": steps,
            
            # Facts and formula
            "extracted_facts": facts,
            "formula": formula,
            
            # Verification details
            "verification_tier": verification_result.tier.value,
            "compliant": verification_result.compliant,
            "confidence": verification_result.confidence,
            "policy_citations": verification_result.policy_citations,
            
            # Tier-specific info
            "procedural_exception": (
                verification_result.procedural_exception.name 
                if verification_result.procedural_exception 
                else None
            ),
            "formal_result": verification_result.formal_result,
            
            # Status
            "compliance_status": compliance_status,
            "method": "Two-Tier: Procedural Exceptions + Formal Verification",
            "verified": verification_result.compliant
        }
    
    except Exception as e:
        import traceback
        return {
            "name": "Two-Tier Pipeline ⭐",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}", traceback.format_exc()],
            "compliance_status": "❌ ERROR",
            "verified": False,
            "error": str(e)
        }
