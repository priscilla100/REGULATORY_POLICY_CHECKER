
from anthropic import Anthropic
import time
import json
import re
import subprocess
import os
from config import get_precis_path, ARITY_MAP
PRECIS_PATH = get_precis_path()

def validate_and_fix_formula(formula: str) -> tuple:
    """Validate and fix formula, return (fixed_formula, warnings, unbound_vars)"""
    
    warnings = []
    
    # Fix: Remove purpose comparison - we don't use purposeIsPurpose
    if ' = @' in formula or '= @' in formula or 'purposeIsPurpose' in formula:
        warnings.append("⚠️ Formula contains purpose comparison, removing it...")
        # Remove "and purpose = @Treatment" or "and purposeIsPurpose(...)"
        formula = re.sub(r'\s+and\s+\w+\s*=\s*@\w+', '', formula)
        formula = re.sub(r'\s+and\s+purposeIsPurpose\([^)]+\)', '', formula)
    
    # Check for unbound variables
    declared_vars = set()
    if formula.startswith("forall"):
        try:
            forall_part = formula.split('.')[0]
            var_list = forall_part.replace("forall", "").strip()
            declared_vars = set(v.strip() for v in var_list.split(','))
        except:
            warnings.append("⚠️ Could not parse forall clause")
    
    # Find all variables in formula body
    all_vars_in_body = set(re.findall(r'\b([a-z_][a-z0-9_]*)\b', formula))
    
    # Remove keywords and predicates
    keywords = {'forall', 'exists', 'and', 'or', 'implies', 'not', 'iff', 'xor', 'true', 'false'}
    predicates = {p.lower() for p in ARITY_MAP.keys()}
    used_vars = all_vars_in_body - keywords - predicates
    
    # Check for unbound variables
    unbound = used_vars - declared_vars
    if unbound:
        warnings.append(f"⚠️ Unbound variables detected: {unbound}, will attempt to fix")
    
    return formula, warnings, list(unbound) if unbound else []

def validate_facts(extracted_facts: list) -> tuple:
    """Validate fact structure and return (valid_facts, warnings)"""
    
    validated_facts = []
    warnings = []
    
    for fact in extracted_facts:
        if not isinstance(fact, list) or len(fact) < 2:
            warnings.append(f"⚠️ Invalid fact structure: {fact}, skipping")
            continue
        
        pred = fact[0]
        args = fact[1:]
        
        # Check if predicate exists
        if pred not in ARITY_MAP:
            warnings.append(f"⚠️ Unknown predicate: {pred}, skipping")
            continue
        
        # Validate arity
        expected_arity = ARITY_MAP[pred]
        if len(args) != expected_arity:
            warnings.append(f"⚠️ {pred} expects {expected_arity} args, got {len(args)}, skipping")
            continue
        
        # Validate constants have @ prefix in purpose positions
        if pred in ['disclose', 'permittedUseOrDisclosure'] and len(args) == 4:
            purpose = args[3]
            if not purpose.startswith('@'):
                warnings.append(f"⚠️ Purpose '{purpose}' missing @, converting to @{purpose}")
                args[3] = f"@{purpose}"
        
        if pred == 'requiredByLaw' and len(args) == 1:
            purpose = args[0]
            if not purpose.startswith('@'):
                warnings.append(f"⚠️ Purpose '{purpose}' missing @, converting to @{purpose}")
                args[0] = f"@{purpose}"
        
        validated_facts.append([pred] + args)
    
    # Ensure minimum facts
    if not validated_facts:
        warnings.append("⚠️ No valid facts extracted, using minimal fallback")
        validated_facts = [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]
    
    return validated_facts, warnings

def safe_metric_value(value):
    """Convert any value to a safe metric value"""
    if isinstance(value, list):
        return len(value)  # Show count for lists
    elif isinstance(value, (int, float)):
        return value
    else:
        return str(value)[:20]  # Truncate long strings

def experiment_pipeline(query: str, client: Anthropic) -> dict:
    """
    Complete pipeline with proper validation and error handling
    """
    start = time.time()
    steps = []
    
    # =====================================
    # STEP 1: LLM1 - Fact Extraction
    # =====================================
    steps.append("🔍 LLM1: Extracting facts from query...")
    
    extract_prompt = f"""You are a HIPAA compliance expert. Extract ALL relevant entities and facts from this question.

Question: {query}

CRITICAL: Extract facts that describe the ACTUAL SCENARIO, not hypothetical rules.

AVAILABLE PREDICATES (use EXACT arity):

1. Entity types (1 arg):
   - coveredEntity(Entity) - hospitals, clinics, providers
   - protectedHealthInfo(Entity) - medical records, x-rays, lab results
   - publicHealthAuthority(Entity) - CDC, health departments

2. Authorization (3 args):
   - hasAuthorization(CoveredEntity, Recipient, PHI)

3. Requirements (1 arg):
   - requiredByLaw(Purpose)

4. Actions (4 args):
   - disclose(From, To, PHI, Purpose) - ALWAYS 4 args!
   - permittedUseOrDisclosure(From, To, PHI, Purpose) - ALWAYS 4 args!

5. Purpose constants (use as CONSTANTS with @):
   - @Treatment, @Payment, @HealthcareOperations
   - @Research, @PublicHealth, @Emergency

CRITICAL RULES:
- disclose() MUST have exactly 4 arguments: (From, To, PHI, Purpose)
- permittedUseOrDisclosure() MUST have exactly 4 arguments: (From, To, PHI, Purpose)
- Purpose is ALWAYS the 4th argument
- Use @Purpose constants with @ prefix
- If disclosure is PERMITTED by HIPAA (like treatment), include permittedUseOrDisclosure fact
- If patient AUTHORIZED it, include hasAuthorization fact
- If REQUIRED by law (like public health), include requiredByLaw fact

EXAMPLES:

Q: "Can a hospital share patient records with a specialist for treatment?"
Facts:
[
    ["coveredEntity", "Hospital1"],
    ["protectedHealthInfo", "MedicalRecord1"],
    ["disclose", "Hospital1", "Specialist1", "MedicalRecord1", "@Treatment"],
    ["permittedUseOrDisclosure", "Hospital1", "Specialist1", "MedicalRecord1", "@Treatment"]
]

Q: "Can a clinic share lab results with researchers if the patient authorized it?"
Facts:
[
    ["coveredEntity", "Clinic1"],
    ["protectedHealthInfo", "LabResult1"],
    ["disclose", "Clinic1", "Researcher1", "LabResult1", "@Research"],
    ["hasAuthorization", "Clinic1", "Researcher1", "LabResult1"]
]

Q: "Can a hospital report infectious disease to public health authorities?"
Facts:
[
    ["coveredEntity", "Hospital1"],
    ["protectedHealthInfo", "LabResult1"],
    ["publicHealthAuthority", "PublicHealthDept1"],
    ["disclose", "Hospital1", "PublicHealthDept1", "LabResult1", "@PublicHealth"],
    ["requiredByLaw", "@PublicHealth"]
]

Q: "Can a provider share x-rays with family without authorization?"
Facts:
[
    ["coveredEntity", "Provider1"],
    ["protectedHealthInfo", "XRay1"],
    ["disclose", "Provider1", "FamilyMember1", "XRay1", "@Research"]
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
            max_tokens=500,
            messages=[{"role": "user", "content": extract_prompt}]
        )
        
        facts_text = message.content[0].text
        
        # Parse JSON
        json_match = re.search(r'\{.*\}', facts_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in LLM response")
        
        facts_json = json.loads(json_match.group())
        extracted_facts = facts_json.get("facts", [])
        
        # Validate facts
        validated_facts, fact_warnings = validate_facts(extracted_facts)
        steps.extend(fact_warnings)
        
        steps.append(f"✅ Extracted and validated {len(validated_facts)} facts")
        
    except Exception as e:
        steps.append(f"❌ Fact extraction failed: {e}")
        validated_facts = [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]
    
    # =====================================
    # STEP 2: LLM1 - Formula Translation
    # =====================================
    steps.append("📐 LLM1: Translating to formal logic...")
    
    translate_prompt = f"""You are translating a compliance question into first-order logic.

Question: {query}
Extracted Facts: {validated_facts}

CRITICAL RULES:
1. Start with "forall" listing ALL variables used in formula
2. Use ONLY these predicates with EXACT arity:
   - coveredEntity(X) [1 arg]
   - protectedHealthInfo(X) [1 arg]
   - publicHealthAuthority(X) [1 arg]
   - hasAuthorization(X,Y,Z) [3 args]
   - requiredByLaw(X) [1 arg]
   - disclose(W,X,Y,Z) [4 args - From, To, PHI, Purpose]
   - permittedUseOrDisclosure(W,X,Y,Z) [4 args - From, To, PHI, Purpose]

3. DO NOT use purposeIsPurpose or any equality checks on purpose
4. Purpose is just a variable - don't filter by it in the formula
5. Use constants with @ prefix: @Treatment, @Research, @PublicHealth
6. ALL variables in formula MUST be in forall clause

USE THIS EXACT TEMPLATE FOR ALL QUERIES:
forall ce, recipient, phi, purpose.
  (coveredEntity(ce)
   and protectedHealthInfo(phi)
   and disclose(ce, recipient, phi, purpose))
  implies
  (permittedUseOrDisclosure(ce, recipient, phi, purpose)
   or hasAuthorization(ce, recipient, phi)
   or requiredByLaw(purpose))

EXAMPLES (ALL questions use the SAME formula):

Q: "Can hospital share data with researchers?"
Formula:
forall ce, recipient, phi, purpose. (coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) implies (permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))

Q: "Can clinic refer patient to specialist for treatment?"
Formula:
forall ce, recipient, phi, purpose. (coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) implies (permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))

Q: "Can hospital report to public health?"
Formula:
forall ce, recipient, phi, purpose. (coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) implies (permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))

Now translate: {query}

CRITICAL: 
- Use the EXACT template above
- DO NOT add "purpose = @Something" anywhere
- DO NOT use purposeIsPurpose
- The purpose checking happens in the FACTS, not the formula

Output ONLY the formula, no explanation:"""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": translate_prompt}]
        )
        
        formula = message.content[0].text.strip()
        
        # Clean up formula
        if "```" in formula:
            match = re.search(r'```.*?\n(.*?)\n```', formula, re.DOTALL)
            if match:
                formula = match.group(1).strip()
        
        formula = formula.split('\n')[0].strip()
        
        # Validate and fix formula
        fixed_formula, formula_warnings, unbound_vars = validate_and_fix_formula(formula)
        steps.extend(formula_warnings)
        
        # If unbound variables detected, ask LLM to fix
        if unbound_vars:
            steps.append(f"🔧 Fixing unbound variables: {unbound_vars}")
            
            fix_prompt = f"""This formula has unbound variables: {unbound_vars}

Formula: {fixed_formula}

Add ALL missing variables to the forall clause at the start.

RULE: Every variable used in the formula body MUST appear in the forall clause.

Example:
BAD:  forall x. ... someVar ...
GOOD: forall x, someVar. ... someVar ...

Output ONLY the corrected formula:"""
            
            fix_message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": fix_prompt}]
            )
            fixed_formula = fix_message.content[0].text.strip()
            steps.append("✅ Formula fixed")
        
        formula = fixed_formula
        steps.append(f"✅ Formula: {formula[:100]}...")
        
    except Exception as e:
        steps.append(f"❌ Formula translation failed: {e}")
        # Fallback to basic template
        formula = "forall ce, recipient, phi, purpose. (coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) implies (permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))"
    
    # =====================================
    # STEP 3: Call OCaml Précis
    # =====================================
    steps.append("⚙️ Calling OCaml Précis engine...")
    
    verified = False
    precis_result = {
        "success": False,
        "output": "",
        "error": "Not executed",
        "pipeline_steps": []
    }
    
    # Prepare facts for OCaml
    facts_for_ocaml = []
    for fact in validated_facts:
        if len(fact) >= 2:
            facts_for_ocaml.append({
                "predicate": fact[0],
                "arguments": fact[1:]
            })
    
    # Wrap formula in policy structure
    wrapped_formula = f"""regulation HIPAA version "1.0"
policy starts
{formula}
;
policy ends"""
    
    # Build request
    precis_request = {
        "formula": wrapped_formula,
        "facts": {
            "facts": facts_for_ocaml
        },
        "regulation": "HIPAA"
    }
    
    try:
        proc = subprocess.Popen(
            [PRECIS_PATH, "json"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(PRECIS_PATH) if os.path.dirname(PRECIS_PATH) else "."
        )
        
        precis_output, precis_error = proc.communicate(
            input=json.dumps(precis_request),
            timeout=30
        )
        
        if proc.returncode == 0 and precis_output.strip():
            try:
                precis_json = json.loads(precis_output)
                
                # Check evaluation result
                if "evaluations" in precis_json and len(precis_json["evaluations"]) > 0:
                    eval_result = precis_json["evaluations"][0].get("evaluation", {})
                    if eval_result.get("result") == "true":
                        verified = True
                    else:
                        verified = False
                
                pipeline_steps = [
                    "✅ Step 1: Parsing (Lexer → Parser → AST)",
                    "✅ Step 2: Type Checking",
                    "✅ Step 3: Evaluation Engine",
                    "✅ Step 4: Results Generated",
                ]
                
                if verified:
                    pipeline_steps.append("✅ Verification: PASSED")
                else:
                    pipeline_steps.append("❌ Verification: FAILED")
                
                precis_result = {
                    "success": True,
                    "output": json.dumps(precis_json, indent=2),
                    "error": "",
                    "pipeline_steps": pipeline_steps,
                    "json_response": precis_json
                }
                
            except json.JSONDecodeError:
                precis_result = {
                    "success": False,
                    "output": precis_output,
                    "error": f"JSON parse failed: {precis_output[:200]}",
                    "pipeline_steps": ["❌ JSON parsing failed"]
                }
        else:
            precis_result = {
                "success": False,
                "output": precis_output,
                "error": precis_error,
                "pipeline_steps": ["❌ Précis execution failed"]
            }
    
    except subprocess.TimeoutExpired:
        precis_result = {
            "success": False,
            "output": "",
            "error": "Timeout (30s)",
            "pipeline_steps": ["❌ Timeout"]
        }
    except Exception as e:
        precis_result = {
            "success": False,
            "output": "",
            "error": str(e),
            "pipeline_steps": [f"❌ Error: {str(e)}"]
        }
    
    steps.append(f"✅ OCaml processing complete")
    
    # =====================================
    # STEP 4: LLM2 - Generate Explanation
    # =====================================
    steps.append("💬 LLM2: Generating explanation...")
    
    explain_prompt = f"""Explain this compliance verification result to a non-technical user.

Question: {query}
Facts Extracted: {validated_facts}
Formula Checked: {formula}
Verification Result: {"PASSED (Compliant)" if verified else "FAILED (Violation)"}

Provide:
1. Direct YES/NO answer to user's question
2. Brief explanation (2-3 sentences) of why
3. Cite specific HIPAA section: §164.502(a)(1)(i)
4. Actionable guidance if needed

Keep it simple and clear."""
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": explain_prompt}]
        )
        explanation = message.content[0].text
    except Exception as e:
        explanation = f"Unable to generate explanation: {e}"
    
    return {
        "name": "Pipeline4Compliance ⭐",
        "answer": explanation,
        "duration": time.time() - start,
        "steps": steps,
        "extracted_facts": validated_facts,
        "formula": formula,
        "precis_result": precis_result,
        "verified": verified,
        "method": "LLM1 (Extract+Translate) → OCaml Précis → LLM2 (Explain)",
        "compliance_status": "✅ COMPLIANT" if verified else "❌ VIOLATION"
    }

