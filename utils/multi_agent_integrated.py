"""
Integrated Multi-Agent System with JSON + FOTL Two-Tier Verification

UPDATED VERSION - Uses:
- JSON policy classification (procedural vs primary)
- Integrated verifier with three tiers
- Policy router for intelligent routing

Architecture:
1. Fact Extractor Agent - Extract structured facts
2. Logic Translator Agent - Convert to formal logic
3. Validator Agent - Validate facts and formula
4. Integrated Two-Tier Verifier Agent - Pattern → LLM+JSON → OCaml+FOTL
5. Explainer Agent - Generate user explanation

This combines multi-agent architecture with integrated two-tier verification.
"""

import re
import json
import time
import subprocess
from typing import List, Dict, Tuple, Optional
from anthropic import Anthropic
import os
from config import get_precis_path, ARITY_MAP
from utils.integrated_verifier import (
    create_integrated_verifier,
    VerificationResult,
    VerificationTier
)

PRECIS_PATH = get_precis_path()

# ============================================================================
# VALIDATION HELPERS
# ============================================================================

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


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class Agent:
    """Base agent with LLM reasoning capability"""
    
    def __init__(self, name: str, role: str, tools: List[str], client: Anthropic):
        self.name = name
        self.role = role
        self.tools = tools
        self.client = client
        self.memory = []
    
    def think(self, prompt: str, max_tokens: int = 1000) -> str:
        """Use LLM to process information"""
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text


# ============================================================================
# FACT EXTRACTOR AGENT
# ============================================================================

class FactExtractorAgent(Agent):
    """Extract structured facts from natural language"""
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Fact Extractor",
            role="HIPAA fact extraction specialist",
            tools=["validate_fact"],
            client=client
        )
    
    def extract(self, query: str) -> List[List[str]]:
        """Extract structured facts from query"""
        
        prompt = f"""Extract HIPAA compliance facts from this question.

Question: {query}

PREDICATES (use EXACT arity):
- coveredEntity(Entity) [1 arg]
- protectedHealthInfo(Entity) [1 arg]
- disclose(From, To, PHI, Purpose) [4 args] - ALWAYS include for action questions
- permittedUseOrDisclosure(From, To, PHI, Purpose) [4 args] - ONLY if explicitly permitted
- hasAuthorization(CE, Recipient, PHI) [3 args] - ONLY if authorization mentioned
- requiredByLaw(Purpose) [1 arg]

PURPOSE CONSTANTS: @Treatment, @Payment, @HealthcareOperations, @Research, @PublicHealth

CRITICAL:
- Always include disclose() for action questions
- Use concrete entity names (Hospital1, Pharmacy1, FamilyMember1, etc.)
- Don't add permittedUseOrDisclosure or hasAuthorization unless explicitly stated

Output ONLY valid JSON:
{{
    "facts": [
        ["predicate", "arg1", "arg2", ...],
        ...
    ]
}}"""
        
        try:
            response = self.think(prompt, max_tokens=800)
            
            json_match = re.search(r'\{.*"facts".*\}', response, re.DOTALL)
            if json_match:
                facts_json = json.loads(json_match.group())
                facts = facts_json.get("facts", [])
                
                # Validate
                validated = []
                for fact in facts:
                    is_valid, msg = validate_fact_structure(fact)
                    if is_valid:
                        validated.append(fact)
                
                return validated if validated else self._get_fallback_facts()
        except Exception as e:
            print(f"❌ Fact extraction error: {e}")
        
        return self._get_fallback_facts()
    
    def _get_fallback_facts(self) -> List[List[str]]:
        """Minimal fallback facts"""
        return [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]


# ============================================================================
# LOGIC TRANSLATOR AGENT
# ============================================================================

class LogicTranslatorAgent(Agent):
    """Translate to first-order logic"""
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Logic Translator",
            role="First-order logic expert",
            tools=["check_formula"],
            client=client
        )
    
    def translate(self, query: str, facts: List[List[str]]) -> str:
        """Generate formula from query and facts"""
        
        # Use standard template for all queries
        return (
            "forall ce, recipient, phi, purpose. "
            "(coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) "
            "implies "
            "(permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))"
        )


# ============================================================================
# VALIDATOR AGENT
# ============================================================================

class ValidatorAgent(Agent):
    """Validate facts and formula"""
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Validator",
            role="Validation specialist",
            tools=["validate_fact", "check_formula"],
            client=client
        )
    
    def validate(self, facts: List[List[str]], formula: str) -> Dict:
        """Validate facts and formula"""
        
        issues = []
        
        # Validate facts
        for fact in facts:
            is_valid, msg = validate_fact_structure(fact)
            if not is_valid:
                issues.append(f"Fact issue: {msg}")
        
        # Validate formula
        if not formula.strip():
            issues.append("Formula is empty")
        elif not formula.startswith("forall"):
            issues.append("Formula should start with 'forall'")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "facts_count": len(facts)
        }


# ============================================================================
# INTEGRATED TWO-TIER VERIFIER AGENT (UPDATED!)
# ============================================================================

class IntegratedTwoTierVerifierAgent(Agent):
    """
    Agent that uses INTEGRATED two-tier verification
    
    Uses:
    - Pattern matching (Tier 1A)
    - LLM + procedural JSON (Tier 1B)
    - OCaml + primary FOTL (Tier 2)
    """
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Integrated Two-Tier Verifier",
            role="JSON + FOTL verification specialist",
            tools=["integrated_verify"],
            client=client
        )
        
        # Create OCaml verifier
        self.ocaml_verifier = self._create_ocaml_verifier()
        
        # UPDATED: Create integrated verifier (uses JSON routing + FOTL)
        self.integrated_verifier = create_integrated_verifier(
            self.client,
            self.ocaml_verifier
        )
    
    def _create_ocaml_verifier(self):
        """Create OCaml Précis verifier"""
        
        class OCamlVerifier:
            def __init__(self, precis_path):
                self.precis_path = precis_path
            
            def verify(self, formula: str, facts: List[List]) -> Dict:
                """Call OCaml Précis"""
                
                if self.precis_path is None:
                    return {
                        "success": False,
                        "verified": False,
                        "error": "Précis not found",
                        "evaluations": [],
                        "violations": []
                    }
                
                try:
                    # Prepare facts
                    facts_for_ocaml = [
                        {"predicate": f[0], "arguments": f[1:]}
                        for f in facts if len(f) >= 2
                    ]
                    
                    # Wrap formula
                    wrapped = f"""regulation HIPAA version "1.0"
policy starts
{formula}
;
policy ends"""
                    
                    # Build request
                    request = {
                        "formula": wrapped,
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
                    
                    output, error = proc.communicate(input=json.dumps(request), timeout=30)
                    
                    if proc.returncode == 0 and output.strip():
                        result = json.loads(output)
                        
                        evaluations = result.get("evaluations", [])
                        violations = result.get("violations", [])
                        
                        verified = all(
                            e.get("evaluation", {}).get("result") == "true"
                            for e in evaluations
                        ) if evaluations else len(violations) == 0
                        
                        return {
                            "success": True,
                            "verified": verified,
                            "evaluations": evaluations,
                            "violations": violations,
                            "json_response": result
                        }
                    else:
                        return {
                            "success": False,
                            "verified": False,
                            "error": error or "OCaml execution failed",
                            "evaluations": [],
                            "violations": []
                        }
                
                except Exception as e:
                    return {
                        "success": False,
                        "verified": False,
                        "error": str(e),
                        "evaluations": [],
                        "violations": []
                    }
        
        return OCamlVerifier(PRECIS_PATH)
    
    def verify(self, query: str, facts: List[List[str]], formula: str) -> VerificationResult:
        """
        Run integrated two-tier verification
        
        Returns:
            VerificationResult with tier information
        """
        
        # UPDATED: Use integrated verifier
        return self.integrated_verifier.verify(query, facts, formula)


# ============================================================================
# EXPLAINER AGENT
# ============================================================================

class ExplainerAgent(Agent):
    """Generate user-friendly explanation"""
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Explainer",
            role="HIPAA compliance explanation specialist",
            tools=["query_hipaa"],
            client=client
        )
    
    def explain(self, query: str, facts: List[List[str]], 
                verification_result: VerificationResult) -> str:
        """Generate explanation based on verification result"""
        
        if verification_result.tier == VerificationTier.TIER_1A_PATTERN:
            # Tier 1A: Pattern match
            prompt = f"""Explain this HIPAA compliance result to a non-technical user.

Question: {query}
Result: COMPLIANT (Pattern Match - Tier 1A)
Exception: {verification_result.procedural_exception.name if verification_result.procedural_exception else 'N/A'}
Policy: {verification_result.procedural_exception.cite if verification_result.procedural_exception else 'N/A'}

Provide:
1. Clear YES answer
2. Brief explanation citing the exception
3. Policy citation
4. Practical guidance

Be clear and reassuring."""
        
        elif verification_result.tier == VerificationTier.TIER_1B_PROCEDURAL:
            # Tier 1B: LLM procedural
            prompt = f"""Explain this HIPAA compliance result to a non-technical user.

Question: {query}
Result: COMPLIANT (LLM Procedural - Tier 1B)
Exception: {verification_result.procedural_exception.name if verification_result.procedural_exception else 'N/A'}
Reason: {verification_result.explanation}

Provide:
1. Clear YES answer
2. Brief explanation
3. Policy citation
4. Practical guidance

Be clear and reassuring."""
        
        else:
            # Tier 2: Formal verification
            prompt = f"""Explain this HIPAA compliance verification to a non-technical user.

Question: {query}
Facts: {json.dumps(facts)}
Result: {"COMPLIANT" if verification_result.compliant else "NON-COMPLIANT"} (Formal Verification - Tier 2)

Provide:
1. Direct YES or NO answer
2. Brief explanation (2-3 sentences)
3. Cite HIPAA section
4. Actionable guidance if needed

Be clear and concise."""
        
        return self.think(prompt, max_tokens=600)


# ============================================================================
# MAIN MULTI-AGENT SYSTEM WITH INTEGRATED TWO-TIER VERIFICATION
# ============================================================================

def multi_agent_with_two_tier_verification(query: str, client: Anthropic, 
                                          all_policies: List[Dict] = None) -> Dict:
    """
    Complete multi-agent system with INTEGRATED two-tier verification
    
    Flow:
    1. Fact Extractor Agent - Extract facts
    2. Logic Translator Agent - Create formula
    3. Validator Agent - Validate
    4. Integrated Two-Tier Verifier Agent - Verify (Pattern → LLM+JSON → OCaml+FOTL)
    5. Explainer Agent - Generate explanation
    
    Returns:
        Complete result dictionary
    """
    
    start = time.time()
    steps = ["🤖 Initializing multi-agent system with integrated two-tier verification..."]
    
    try:
        # ===================================================================
        # INITIALIZATION
        # ===================================================================
        
        fact_extractor = FactExtractorAgent(client)
        logic_translator = LogicTranslatorAgent(client)
        validator = ValidatorAgent(client)
        integrated_verifier = IntegratedTwoTierVerifierAgent(client)  # UPDATED!
        explainer = ExplainerAgent(client)
        
        # ===================================================================
        # STEP 1: FACT EXTRACTION
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 1: Fact Extractor Agent...")
        
        facts = fact_extractor.extract(query)
        
        steps.append(f"✅ Extracted {len(facts)} facts:")
        for fact in facts:
            steps.append(f"   • {fact}")
        
        # ===================================================================
        # STEP 2: LOGIC TRANSLATION
        # ===================================================================
        
        steps.append("")
        steps.append("📐 STEP 2: Logic Translator Agent...")
        
        formula = logic_translator.translate(query, facts)
        
        steps.append(f"✅ Formula: {formula[:100]}...")
        
        # ===================================================================
        # STEP 3: VALIDATION
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 3: Validator Agent...")
        
        validation = validator.validate(facts, formula)
        
        if validation['valid']:
            steps.append("✅ Validation passed")
        else:
            steps.append(f"⚠️ Validation issues: {validation['issues']}")
        
        # ===================================================================
        # STEP 4: INTEGRATED TWO-TIER VERIFICATION (UPDATED!)
        # ===================================================================
        
        steps.append("")
        steps.append("⚙️ STEP 4: Integrated Two-Tier Verifier Agent...")
        
        verification_result = integrated_verifier.verify(query, facts, formula)
        
        if verification_result.tier == VerificationTier.TIER_1A_PATTERN:
            steps.append("✅ Tier 1A: Pattern Match")
            if verification_result.procedural_exception:
                steps.append(f"   Exception: {verification_result.procedural_exception.name}")
                steps.append(f"   Policy: {verification_result.procedural_exception.cite}")
            steps.append(f"   Confidence: {verification_result.confidence:.2%}")
            steps.append("   → Compliance confirmed without formal verification")
        
        elif verification_result.tier == VerificationTier.TIER_1B_PROCEDURAL:
            steps.append("✅ Tier 1B: LLM Procedural Classification")
            if verification_result.procedural_exception:
                steps.append(f"   Exception: {verification_result.procedural_exception.name}")
            steps.append(f"   Confidence: {verification_result.confidence:.2%}")
            steps.append("   → Procedural exception confirmed")
        
        else:
            steps.append("   Tier 1: No procedural exception")
            steps.append("   → Tier 2: Formal Verification")
            
            if verification_result.formal_result:
                if verification_result.formal_result.get('success'):
                    steps.append(f"✅ OCaml Précis: {'COMPLIANT' if verification_result.compliant else 'NON-COMPLIANT'}")
                else:
                    steps.append(f"❌ OCaml failed: {verification_result.formal_result.get('error', 'Unknown')}")
        
        # ===================================================================
        # STEP 5: EXPLANATION
        # ===================================================================
        
        steps.append("")
        steps.append("💬 STEP 5: Explainer Agent...")
        
        explanation = explainer.explain(query, facts, verification_result)
        
        steps.append("✅ Explanation generated")
        
        # ===================================================================
        # FINAL RESULT
        # ===================================================================
        
        compliance_status = "✅ COMPLIANT" if verification_result.compliant else "❌ VIOLATION"
        
        return {
            "name": "Multi-Agent + Integrated Two-Tier 🚀",
            "answer": explanation,
            "duration": time.time() - start,
            "steps": steps,
            
            # Facts and formula
            "extracted_facts": facts,
            "formula": formula,
            
            # Verification
            "verification_tier": verification_result.tier.value,
            "compliant": verification_result.compliant,
            "confidence": verification_result.confidence,
            "policy_citations": verification_result.policy_citations,
            
            # Tier-specific
            "procedural_exception": (
                verification_result.procedural_exception.name 
                if verification_result.procedural_exception 
                else None
            ),
            "formal_result": verification_result.formal_result,
            
            # Status
            "compliance_status": compliance_status,
            "method": "Multi-Agent + Integrated (JSON + Pattern + LLM + FOTL)",
            "verified": verification_result.compliant
        }
    
    except Exception as e:
        import traceback
        return {
            "name": "Multi-Agent + Integrated Two-Tier 🚀",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}", traceback.format_exc()],
            "compliance_status": "❌ ERROR",
            "verified": False,
            "error": str(e)
        }
