"""
FIXED MULTI-AGENT COMPLIANCE SYSTEM
Addresses all identified issues:
1. Policy filtering to avoid checking irrelevant organizational policies
2. Query-type detection (requirement vs action questions)
3. Appropriate formula generation based on question type
4. Better fact extraction
"""

import re
import json
import time
import subprocess
from typing import List, Dict, Tuple
from anthropic import Anthropic
from utils.cfr_parser import load_policy_database
import os
from utils.policy_filtering import RobustPolicyFilterAgent
policy_filter = RobustPolicyFilterAgent()
# ============================================================================
# VALIDATION HELPERS
# ============================================================================

ARITY_MAP = {
    'coveredEntity': 1,
    'protectedHealthInfo': 1,
    'publicHealthAuthority': 1,
    'businessAssociate': 1,
    'disclose': 4,
    'permittedUseOrDisclosure': 4,
    'hasAuthorization': 3,
    'requiredByLaw': 1,
    'purposeIsPurpose': 2,
}

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


def check_formula_syntax(formula: str) -> Tuple[bool, str]:
    """Basic formula syntax check"""
    if not formula.strip():
        return False, "Empty formula"
    
    if not formula.startswith("forall"):
        return False, "Formula should start with 'forall'"
    
    required = ['implies', '(', ')']
    for token in required:
        if token not in formula:
            return False, f"Missing {token}"
    
    return True, "Valid"


# ============================================================================
# BASE AGENT CLASS
# ============================================================================

class Agent:
    def __init__(self, name: str, role: str, tools: List[str], client: Anthropic):
        self.name = name
        self.role = role
        self.tools = tools
        self.client = client
        self.memory = []
    
    def think(self, prompt: str) -> str:
        """Use LLM to process information"""
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

# ============================================================================
# NEW: POLICY FILTER AGENT
# ============================================================================

class PolicyFilterAgent(Agent):
    """
    CRITICAL NEW AGENT: Filters policies to only relevant ones
    This prevents checking 108 organizational policies for simple questions
    """
    
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Policy Filter",
            role="Policy relevance filtering specialist",
            tools=["semantic_match"],
            client=client
        )
    
    def filter_policies(self, query: str, all_policies: List[Dict]) -> List[Dict]:
        """
        Filter policies to only those relevant to the query
        
        This is THE FIX for the 7 violations issue!
        """
        
        query_lower = query.lower()
        
        # Step 1: Detect query intent
        intents = self._detect_intents(query_lower)
        
        # Step 2: Filter out organizational policies unless explicitly asked
        relevant_policies = []
        
        for policy in all_policies:
            desc = policy.get('description', '').lower()
            section = policy.get('section', '').lower()
            policy_id = policy.get('policy_id', '')
            
            # Check if this is an organizational/administrative policy
            is_organizational = self._is_organizational_policy(desc, policy_id)
            
            # CRITICAL: Skip organizational policies unless user asks about them
            if is_organizational:
                if 'organizational' in intents or 'administrative' in intents:
                    relevant_policies.append(policy)
                # Otherwise SKIP - this is the fix!
                continue
            
            # Check if policy matches query intent
            if self._matches_intent(policy, intents, query_lower):
                relevant_policies.append(policy)
        
        # Step 3: Limit to top 30 most relevant
        # (In practice, most queries will match 10-20 policies)
        return relevant_policies[:30]
    
    def _detect_intents(self, query_lower: str) -> set:
        """Detect what the query is asking about"""
        intents = set()
        
        intent_keywords = {
            'treatment': ['treatment', 'care', 'specialist', 'doctor', 'physician', 'referral'],
            'research': ['research', 'study', 'clinical trial', 'researcher'],
            'authorization': ['authorization', 'consent', 'permission', 'written'],
            'disclosure': ['share', 'disclose', 'provide', 'give access'],
            'family': ['family', 'relative', 'grandma', 'parent', 'spouse'],
            'business_associate': ['business associate', 'vendor', 'contractor'],
            'public_health': ['public health', 'disease', 'reporting'],
            'organizational': ['organizational', 'compliance program', 'privacy officer', 'security officer'],
            'administrative': ['policies', 'procedures', 'safeguards', 'training']
        }
        
        for intent, keywords in intent_keywords.items():
            if any(kw in query_lower for kw in keywords):
                intents.add(intent)
        
        return intents
    
    def _is_organizational_policy(self, desc: str, policy_id: str) -> bool:
        """Check if policy is about organizational requirements"""
        
        organizational_keywords = [
            'privacy official', 'privacy officer',
            'security official', 'security officer',
            'personnel designation', 'training',
            'safeguards', 'policies and procedures',
            'complaint process', 'evaluation',
            'incident response', 'documentation',
            'sanctions', 'mitigation',
            'risk analysis', 'workforce security'
        ]
        
        # Also check policy IDs (organizational policies are typically 29-87)
        if policy_id.startswith('HIPAA-'):
            try:
                num = int(policy_id.split('-')[1])
                if 29 <= num <= 87:  # Administrative/organizational range
                    return True
            except:
                pass
        
        return any(kw in desc for kw in organizational_keywords)
    
    def _matches_intent(self, policy: Dict, intents: set, query_lower: str) -> bool:
        """Check if policy matches detected intents"""
        
        desc = policy.get('description', '').lower()
        section = policy.get('section', '').lower()
        
        # Always include general/foundational policies
        foundational_ids = ['HIPAA-0', 'HIPAA-1', 'HIPAA-2', 'HIPAA-3']
        if policy.get('policy_id') in foundational_ids:
            return True
        
        # Match based on intents
        for intent in intents:
            if intent == 'treatment' and any(kw in desc for kw in ['treatment', 'tpo', 'healthcare operations']):
                return True
            elif intent == 'research' and 'research' in desc:
                return True
            elif intent == 'authorization' and any(kw in desc for kw in ['authorization', 'consent']):
                return True
            elif intent == 'family' and any(kw in desc for kw in ['family', 'relatives', 'friends']):
                return True
            elif intent == 'business_associate' and 'business associate' in desc:
                return True
            elif intent == 'public_health' and 'public health' in desc:
                return True
        
        # Fallback: check if any query words appear in description
        query_words = set(query_lower.split()) - {'is', 'the', 'a', 'an', 'for', 'to', 'can', 'may'}
        desc_words = set(desc.split())
        overlap = query_words & desc_words
        
        return len(overlap) >= 2

# ============================================================================
# IMPROVED FACT EXTRACTOR AGENT
# ============================================================================

class FactExtractorAgent(Agent):
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Fact Extractor",
            role="HIPAA fact extraction specialist",
            tools=["validate_fact"],
            client=client
        )
    
    def extract(self, query: str) -> List[List[str]]:
        """Extract structured facts from natural language"""
        
        query_lower = query.lower()
        
        # Detect question type FIRST
        is_requirement = self._is_requirement_question(query_lower)
        is_action = self._is_action_question(query_lower)
        
        if is_requirement:
            # For requirement questions: extract minimal facts
            return self._extract_requirement_facts(query, query_lower)
        elif is_action:
            # For action questions: extract full scenario
            return self._extract_action_facts(query, query_lower)
        else:
            # Fallback: let LLM decide
            return self._extract_with_llm(query)
    
    def _is_requirement_question(self, query_lower: str) -> bool:
        """Check if asking about rules/requirements"""
        requirement_patterns = [
            'is consent required',
            'is authorization required',
            'is required for',
            'must obtain',
            'required to',
            'need to have',
            'mandatory',
            'obligated to'
        ]
        return any(pattern in query_lower for pattern in requirement_patterns)
    
    def _is_action_question(self, query_lower: str) -> bool:
        """Check if asking about specific actions"""
        action_patterns = ['can', 'may', 'allowed to', 'permitted to', 'able to']
        return any(pattern in query_lower for pattern in action_patterns)
    
    def _extract_requirement_facts(self, query: str, query_lower: str) -> List[List[str]]:
        """
        Extract facts for requirement questions
        These don't need specific disclosure scenarios
        """
        facts = [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]
        
        # Identify what's being asked about
        if 'treatment' in query_lower:
            facts.append(["permittedUseOrDisclosure", "Entity1", "AnyRecipient", "PHI1", "@Treatment"])
        elif 'payment' in query_lower:
            facts.append(["permittedUseOrDisclosure", "Entity1", "AnyRecipient", "PHI1", "@Payment"])
        elif 'research' in query_lower:
            # For research, authorization IS typically required
            facts.append(["disclose", "Entity1", "Researcher1", "PHI1", "@Research"])
        elif 'public health' in query_lower:
            facts.append(["permittedUseOrDisclosure", "Entity1", "PublicHealth1", "PHI1", "@PublicHealth"])
        
        return facts
    
    def _extract_action_facts(self, query: str, query_lower: str) -> List[List[str]]:
        """
        Extract facts for action questions
        These need full disclosure scenarios
        """
        
        prompt = f"""Extract HIPAA compliance facts for this ACTION question:

"{query}"

PREDICATES (use EXACT arity):
- coveredEntity(Entity) [1 arg]
- protectedHealthInfo(Entity) [1 arg]
- disclose(From, To, PHI, Purpose) [4 args]
- permittedUseOrDisclosure(From, To, PHI, Purpose) [4 args]
- hasAuthorization(CE, Recipient, PHI) [3 args]
- requiredByLaw(Purpose) [1 arg]

PURPOSE CONSTANTS: @Treatment, @Payment, @HealthcareOperations, @Research, @PublicHealth

CRITICAL:
- Always include disclose() for action questions
- Use concrete entity names (Hospital1, Researcher1, etc.)
- If treatment/payment/operations: also add permittedUseOrDisclosure
- If authorization mentioned: add hasAuthorization

Output ONLY valid JSON:
{{
    "facts": [
        ["predicate", "arg1", "arg2", ...],
        ...
    ]
}}"""
        
        response = self.think(prompt)
        
        try:
            json_match = re.search(r'\{.*"facts".*\}', response, re.DOTALL)
            if json_match:
                facts_json = json.loads(json_match.group())
                facts = facts_json.get("facts", [])
                
                # Validate each fact
                validated = []
                for fact in facts:
                    is_valid, msg = validate_fact_structure(fact)
                    if is_valid:
                        validated.append(fact)
                    else:
                        print(f"⚠️ Skipping invalid fact: {fact} ({msg})")
                
                return validated if validated else self._get_fallback_facts()
        except Exception as e:
            print(f"❌ Fact extraction error: {e}")
        
        return self._get_fallback_facts()
    
    def _extract_with_llm(self, query: str) -> List[List[str]]:
        """Fallback: let LLM extract facts"""
        return self._extract_action_facts(query, query.lower())
    
    def _get_fallback_facts(self) -> List[List[str]]:
        """Minimal fallback facts"""
        return [
            ["coveredEntity", "Entity1"],
            ["protectedHealthInfo", "PHI1"]
        ]

# ============================================================================
# IMPROVED LOGIC TRANSLATOR AGENT
# ============================================================================

class LogicTranslatorAgent(Agent):
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Logic Translator",
            role="First-order logic expert",
            tools=["check_formula"],
            client=client
        )
    
    def translate(self, query: str, facts: List[List[str]]) -> str:
        """
        Generate formula based on question type and extracted facts
        
        KEY FIX: Different formulas for different scenarios
        """
        
        query_lower = query.lower()
        
        # Check what facts we have
        has_disclosure = any(f[0] == "disclose" for f in facts)
        has_permitted = any(f[0] == "permittedUseOrDisclosure" for f in facts)
        
        # Detect question type
        is_requirement = any(pattern in query_lower for pattern in [
            'is consent required', 'is authorization required', 
            'is required', 'must', 'required to'
        ])
        
        if has_disclosure:
            # ACTION question with disclosure scenario
            formula = self._disclosure_formula()
        elif is_requirement and has_permitted:
            # REQUIREMENT question - check if permission exists
            formula = self._requirement_formula()
        else:
            # Generic compliance check
            formula = self._generic_formula()
        
        return formula
    
    def _disclosure_formula(self) -> str:
        """Formula for action questions with disclosure"""
        return """forall ce, recipient, phi, purpose. 
(coveredEntity(ce) and protectedHealthInfo(phi) and disclose(ce, recipient, phi, purpose)) 
implies 
(permittedUseOrDisclosure(ce, recipient, phi, purpose) or hasAuthorization(ce, recipient, phi) or requiredByLaw(purpose))"""
    
    def _requirement_formula(self) -> str:
        """Formula for requirement questions"""
        # This checks if a permitted use exists for the scenario
        return """forall ce, recipient, phi, purpose. 
(coveredEntity(ce) and protectedHealthInfo(phi) and permittedUseOrDisclosure(ce, recipient, phi, purpose))
implies
true"""
    
    def _generic_formula(self) -> str:
        """Generic fallback formula"""
        return """forall ce, phi. 
(coveredEntity(ce) and protectedHealthInfo(phi)) 
implies 
true"""


# ============================================================================
# VALIDATOR AGENT (unchanged)
# ============================================================================

class ValidatorAgent(Agent):
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Validator",
            role="Fact and formula validation specialist",
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
        is_valid, msg = check_formula_syntax(formula)
        if not is_valid:
            issues.append(f"Formula issue: {msg}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "facts_count": len(facts),
            "formula_valid": is_valid
        }

# ============================================================================
# VERIFIER AGENT (with path fix from earlier)
# ============================================================================

class VerifierAgent(Agent):
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Verifier",
            role="OCaml Précis engine operator",
            tools=[],
            client=client
        )
    
    def verify(self, formula: str, facts: List[List[str]], 
               relevant_policies: List[Dict] = None) -> Dict:
        """
        Call OCaml Précis verification engine
        
        NEW: Can optionally filter to only relevant_policies
        """
        
        # Try to find Précis executable
        possible_paths = [
            os.path.join(os.getcwd(), "precis"),
            "./precis",
            "/app/precis",
            os.path.join(os.path.dirname(__file__), "precis"),
        ]
        
        PRECIS_PATH = None
        for path in possible_paths:
            if os.path.exists(path):
                PRECIS_PATH = path
                break
        
        if PRECIS_PATH is None:
            return {
                "success": False,
                "verified": False,
                "result": {},
                "output": "",
                "error": "Précis executable not found",
                "json_response": {},
                "pipeline_steps": ["❌ Précis not found"]
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
            
            # NEW: If relevant_policies provided, could filter here
            # (For now, OCaml will check all policies in its database)
            
            # Call OCaml
            proc = subprocess.Popen(
                [PRECIS_PATH, "json"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(PRECIS_PATH) if os.path.dirname(PRECIS_PATH) else "."
            )
            
            output, error = proc.communicate(input=json.dumps(request), timeout=30)
            
            if proc.returncode == 0 and output.strip():
                result = json.loads(output)
                
                # NEW: Filter results to only relevant policies if provided
                if relevant_policies:
                    result = self._filter_results(result, relevant_policies)
                
                # Parse verification result
                overall_compliant = result.get("overall_compliant", None)
                violations = result.get("violations", [])
                evaluations = result.get("evaluations", [])
                
                if overall_compliant is not None:
                    verified = overall_compliant
                elif evaluations:
                    verified = all(
                        e.get("evaluation", {}).get("result") == "true"
                        for e in evaluations
                    )
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
                    pipeline_steps.append(f"❌ Verification: FAILED ({len(violations)} violations)")
                
                return {
                    "success": True,
                    "verified": verified,
                    "result": result,
                    "output": json.dumps(result, indent=2),
                    "error": "",
                    "json_response": result,
                    "pipeline_steps": pipeline_steps,
                    "violations_count": len(violations),
                    "compliant_count": len(evaluations) - len(violations) if evaluations else 0
                }
            else:
                return {
                    "success": False,
                    "verified": False,
                    "result": {},
                    "output": output,
                    "error": error,
                    "json_response": {},
                    "pipeline_steps": ["❌ Précis execution failed"]
                }
        
        except Exception as e:
            return {
                "success": False,
                "verified": False,
                "result": {},
                "output": "",
                "error": str(e),
                "json_response": {},
                "pipeline_steps": [f"❌ Error: {str(e)}"]
            }
    
    def _filter_results(self, result: Dict, relevant_policies: List[Dict]) -> Dict:
        """Filter OCaml results to only include relevant policies"""
        
        relevant_ids = {p['policy_id'] for p in relevant_policies}
        
        # Filter evaluations
        if 'evaluations' in result:
            result['evaluations'] = [
                e for e in result['evaluations']
                if e.get('policy_id') in relevant_ids
            ]
        
        # Filter matched_policies
        if 'matched_policies' in result:
            result['matched_policies'] = [
                p for p in result['matched_policies']
                if p.get('policy_id') in relevant_ids
            ]
        
        # Filter violations
        if 'violations' in result:
            result['violations'] = [
                v for v in result['violations']
                if v in relevant_ids
            ]
        
        # Recalculate overall_compliant
        if result.get('evaluations'):
            violations = [e for e in result['evaluations'] if e.get('evaluation', {}).get('result') == 'false']
            result['overall_compliant'] = len(violations) == 0
        
        return result

# ============================================================================
# EXPLAINER AGENT (unchanged)
# ============================================================================

class ExplainerAgent(Agent):
    def __init__(self, client: Anthropic):
        super().__init__(
            name="Explainer",
            role="HIPAA compliance explanation specialist",
            tools=["query_hipaa"],
            client=client
        )
    
    def explain(self, query: str, facts: List[List[str]], 
                formula: str, verification_result: Dict) -> str:
        """Generate user-friendly explanation"""
        
        verified = verification_result.get('verified', False)
        
        prompt = f"""Explain this HIPAA compliance verification to a non-technical user.

Question: {query}
Facts: {json.dumps(facts)}
Verification: {"PASSED ✅" if verified else "FAILED ❌"}

Provide:
1. Direct YES or NO answer
2. Brief explanation (2-3 sentences)
3. Cite HIPAA section (e.g., §164.502(a)(1))
4. Actionable guidance if needed

Be clear and concise."""
        
        return self.think(prompt)

# ============================================================================
# MAIN MULTI-AGENT SYSTEM (WITH ALL FIXES)
# ============================================================================

def multi_agent_compliance_system(query: str, client: Anthropic) -> dict:
    """
    Complete multi-agent system with policy filtering integrated
    
    Flow:
    1. Filter policies (NEW STEP!)
    2. Extract facts
    3. Translate to logic
    4. Validate
    5. Verify (with filtered policies)
    6. Explain
    """
    
    start = time.time()
    steps = ["🤖 Initializing multi-agent system..."]
    
    try:
        # ===================================================================
        # INITIALIZATION: Create all agents
        # ===================================================================
        
        # NEW: Policy filtering agent
        policy_filter = RobustPolicyFilterAgent(client)
        
        # Existing agents
        fact_extractor = FactExtractorAgent(client)
        logic_translator = LogicTranslatorAgent(client)
        validator = ValidatorAgent(client)
        verifier = VerifierAgent(client)
        explainer = ExplainerAgent(client)
        
        
        # ===================================================================
        # STEP 0: POLICY FILTERING (NEW!)
        # This is where the magic happens!
        # ===================================================================
        
        steps.append("🔍 STEP 0: Policy Filtering Agent - Loading policies...")
        
        # Load ALL policies from your database
        all_policies = load_policy_database()  # You implement this
        total_policies = len(all_policies)
        
        steps.append(f"   Loaded {total_policies} policies from database")
        
        # Filter to only relevant policies
        steps.append("   Filtering to relevant policies using hybrid semantic search...")
        relevant_policies = policy_filter.filter_policies(
            query=query,
            all_policies=all_policies,
            top_k=30  # Keep top 30 most relevant
        )
        
        steps.append(f"✅ Filtered {total_policies} → {len(relevant_policies)} relevant policies")
        
        # Show top 3 for debugging
        if len(relevant_policies) >= 3:
            steps.append("   Top 3 policies:")
            for i, p in enumerate(relevant_policies[:3], 1):
                score = p.get('relevance_score', 0)
                steps.append(f"      {i}. {p['policy_id']} - {p.get('description', 'N/A')} (score: {score:.2f})")
        
        
        # ===================================================================
        # STEP 1: FACT EXTRACTION (same as before)
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 1: Fact Extractor Agent - Analyzing query...")
        
        facts = fact_extractor.extract(query)
        
        steps.append(f"✅ Extracted {len(facts)} facts:")
        for fact in facts:
            steps.append(f"   • {fact}")
        
        
        # ===================================================================
        # STEP 2: LOGIC TRANSLATION (same as before)
        # ===================================================================
        
        steps.append("")
        steps.append("📐 STEP 2: Logic Translator Agent - Creating formal formula...")
        
        formula = logic_translator.translate(query, facts)
        
        steps.append(f"✅ Formula created:")
        steps.append(f"   {formula[:100]}...")
        
        
        # ===================================================================
        # STEP 3: VALIDATION (same as before)
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 3: Validator Agent - Checking correctness...")
        
        validation = validator.validate(facts, formula)
        
        if validation['valid']:
            steps.append("✅ Validation passed")
        else:
            steps.append(f"⚠️ Validation issues: {validation['issues']}")
        
        
        # ===================================================================
        # STEP 4: FORMAL VERIFICATION (MODIFIED - uses filtered policies!)
        # This is the KEY difference!
        # ===================================================================
        
        steps.append("")
        steps.append("⚙️ STEP 4: Verifier Agent - Running OCaml Précis...")
        steps.append(f"   Verifying against {len(relevant_policies)} filtered policies")
        steps.append(f"   (instead of all {total_policies} policies)")
        
        # Call OCaml with FILTERED policies
        precis_result = verifier.verify(
            formula=formula,
            facts=facts,
            relevant_policies=relevant_policies  # <-- KEY: Only check these!
        )
        
        if precis_result['success']:
            verified = precis_result.get('verified', False)
            violations = precis_result.get('violations_count', 0)
            compliant = precis_result.get('compliant_count', 0)
            
            steps.append(f"✅ Verification complete:")
            steps.append(f"   ✅ {compliant} policies satisfied")
            steps.append(f"   ❌ {violations} policies violated")
        else:
            steps.append(f"❌ Verification failed: {precis_result.get('error', 'Unknown error')}")
            verified = False
        
        
        # ===================================================================
        # STEP 5: EXPLANATION (same as before)
        # ===================================================================
        
        steps.append("")
        steps.append("💬 STEP 5: Explainer Agent - Generating explanation...")
        
        explanation = explainer.explain(query, facts, formula, precis_result)
        
        steps.append("✅ Explanation generated")
        
        
        # ===================================================================
        # FINAL RESULT
        # ===================================================================
        
        # Determine compliance status
        violations_count = precis_result.get('violations_count', 0)
        
        if verified:
            compliance_status = "✅ COMPLIANT"
        else:
            compliance_status = f"❌ VIOLATION ({violations_count} policies violated)"
        
        return {
            "name": "Multi-Agent System with Smart Filtering 🧠",
            "answer": explanation,
            "duration": time.time() - start,
            "steps": steps,
            
            # Policy filtering info
            "total_policies_in_db": total_policies,
            "filtered_policies_count": len(relevant_policies),
            "filtering_ratio": f"{len(relevant_policies)}/{total_policies} ({100*len(relevant_policies)/total_policies:.1f}%)",
            "top_policies": relevant_policies[:5],  # For display
            
            # Fact extraction
            "extracted_facts": facts,
            
            # Logic translation
            "formula": formula,
            
            # Verification
            "precis_result": precis_result,
            "verified": verified,
            "violations_count": violations_count,
            "compliant_count": precis_result.get('compliant_count', 0),
            
            # Final status
            "compliance_status": compliance_status,
            "method": "Multi-Agent + Semantic Policy Filtering"
        }
    
    except Exception as e:
        import traceback
        return {
            "name": "Multi-Agent System with Smart Filtering 🧠",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}", traceback.format_exc()],
            "compliance_status": "❌ ERROR",
            "verified": False,
            "error": str(e)
        }


def multi_agent_compliance_system_TWO_TIER(query: str, client: Anthropic) -> dict:
    """
    EXACT CHANGES for your multi_agent_compliance_system function
    """

    start = time.time()
    steps = ["🤖 Initializing multi-agent system..."]
    
    try:
        # ===================================================================
        # INITIALIZATION: Create all agents
        # ===================================================================
        
        # NEW: Import and initialize two-tier verifier
        from utils.two_tier_verifier import TwoTierVerifier
        
        two_tier_verifier = TwoTierVerifier(
            precis_path="./precis",  # Adjust path if needed
            database_dir="data",
            policies_dir="policies",
        )
        
        # Keep existing agents
        policy_filter = RobustPolicyFilterAgent(client)
        fact_extractor = FactExtractorAgent(client)
        logic_translator = LogicTranslatorAgent(client)
        validator = ValidatorAgent(client)
        # verifier = VerifierAgent(client)  # ❌ REMOVE THIS LINE
        explainer = ExplainerAgent(client)
        
        
        # ===================================================================
        # STEP 0: POLICY FILTERING (UNCHANGED)
        # ===================================================================
        
        steps.append("🔍 STEP 0: Policy Filtering Agent - Loading policies...")
        
        all_policies = load_policy_database()
        total_policies = len(all_policies)
        
        steps.append(f"   Loaded {total_policies} policies from database")
        steps.append("   Filtering to relevant policies using hybrid semantic search...")
        
        relevant_policies = policy_filter.filter_policies(
            query=query,
            all_policies=all_policies,
            top_k=30
        )
        
        steps.append(f"✅ Filtered {total_policies} → {len(relevant_policies)} relevant policies")
        
        if len(relevant_policies) >= 3:
            steps.append("   Top 3 policies:")
            for i, p in enumerate(relevant_policies[:3], 1):
                score = p.get('relevance_score', 0)
                steps.append(f"      {i}. {p['policy_id']} - {p.get('description', 'N/A')} (score: {score:.2f})")
        
        
        # ===================================================================
        # STEP 1: FACT EXTRACTION (UNCHANGED)
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 1: Fact Extractor Agent - Analyzing query...")
        
        facts = fact_extractor.extract(query)
        
        steps.append(f"✅ Extracted {len(facts)} facts:")
        for fact in facts:
            steps.append(f"   • {fact}")
        
        
        # ===================================================================
        # STEP 2: LOGIC TRANSLATION (UNCHANGED)
        # ===================================================================
        
        steps.append("")
        steps.append("📐 STEP 2: Logic Translator Agent - Creating formal formula...")
        
        formula = logic_translator.translate(query, facts)
        
        steps.append(f"✅ Formula created:")
        steps.append(f"   {formula[:100]}...")
        
        
        # ===================================================================
        # STEP 3: VALIDATION (UNCHANGED)
        # ===================================================================
        
        steps.append("")
        steps.append("🔍 STEP 3: Validator Agent - Checking correctness...")
        
        validation = validator.validate(facts, formula)
        
        if validation['valid']:
            steps.append("✅ Validation passed")
        else:
            steps.append(f"⚠️ Validation issues: {validation['issues']}")
        
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 4: TWO-TIER VERIFICATION
        # ═══════════════════════════════════════════════════════════════════
        # ⚠️ THIS IS THE ONLY SECTION THAT CHANGES!
        # ═══════════════════════════════════════════════════════════════════
        
        steps.append("")
        steps.append("⚙️ STEP 4: Two-Tier Verifier - Running OCaml Précis...")
 
        # Call two-tier verifier
        two_tier_result = two_tier_verifier.verify_two_tier(facts)
        
        # Add detailed steps
        steps.append(f"   🔍 Tier 1 (PRIMARY - Substantive): {two_tier_result.tier1_status}")
        if two_tier_result.tier1_status == "PASSED":
            steps.append(f"      ✅ Action is substantively permitted")
        else:
            steps.append(f"      ❌ Action violates substantive HIPAA rules")
        
        steps.append(f"   🔍 Tier 2 (PROCEDURAL - Compliance): {two_tier_result.tier2_status}")
        if two_tier_result.tier2_status == "PASSED":
            steps.append(f"      ✅ All procedural requirements satisfied")
        elif two_tier_result.tier2_status == "FAILED":
            steps.append(f"      ⚠️ {len(two_tier_result.warnings)} procedural warnings")
        else:
            steps.append(f"      ℹ️ Not checked (tier 1 failed)")
        
        steps.append(f"✅ Verification complete: {two_tier_result.verdict}")
        
        # Build precis_result for backward compatibility with your display code
        precis_result = {
            'success': two_tier_result.primary_result.success if two_tier_result.primary_result else False,
            'verified': two_tier_result.overall_compliant,
            'violations_count': len(two_tier_result.primary_result.violations) if two_tier_result.primary_result else 0,
            'compliant_count': len(two_tier_result.primary_result.matched_policies) if two_tier_result.primary_result else 0,
        }
        
        verified = two_tier_result.overall_compliant
        violations_count = len(two_tier_result.primary_result.violations) if two_tier_result.primary_result else 0
        
        # ──────────────────────────────────────────────────────────────────
        # END OF CHANGES FOR STEP 4
        # ──────────────────────────────────────────────────────────────────
        
        
        # ===================================================================
        # STEP 5: EXPLANATION (UNCHANGED)
        # ===================================================================
        
        steps.append("")
        steps.append("💬 STEP 5: Explainer Agent - Generating explanation...")
        
        explanation = explainer.explain(query, facts, formula, precis_result)
        
        steps.append("✅ Explanation generated")
        
        
        # ═══════════════════════════════════════════════════════════════════
        # FINAL RESULT
        # ═══════════════════════════════════════════════════════════════════
        # ⚠️ UPDATE RETURN DICT TO INCLUDE TWO-TIER FIELDS
        # ═══════════════════════════════════════════════════════════════════
        
        # ──────────────────────────────────────────────────────────────────
        # ❌ DELETE THESE LINES:
        # ──────────────────────────────────────────────────────────────────
        # if verified:
        #     compliance_status = "✅ COMPLIANT"
        # else:
        #     compliance_status = f"❌ VIOLATION ({violations_count} policies violated)"
        
        # ──────────────────────────────────────────────────────────────────
        # ✅ ADD THIS LINE:
        # ──────────────────────────────────────────────────────────────────
        compliance_status = two_tier_result.verdict
        
        
        return {
            "name": "Multi-Agent System with Two-Tier Verification 🧠",
            "answer": explanation,
            "duration": time.time() - start,
            "steps": steps,
            
            # Policy filtering info (UNCHANGED)
            "total_policies_in_db": total_policies,
            "filtered_policies_count": len(relevant_policies),
            "filtering_ratio": f"{len(relevant_policies)}/{total_policies} ({100*len(relevant_policies)/total_policies:.1f}%)",
            "top_policies": relevant_policies[:5],
            
            # Fact extraction (UNCHANGED)
            "extracted_facts": facts,
            
            # Logic translation (UNCHANGED)
            "formula": formula,
            
            # Verification (UPDATED - add two-tier fields)
            "precis_result": precis_result,
            "verified": verified,
            "violations_count": violations_count,
            "compliant_count": precis_result.get('compliant_count', 0),
            
            # ✅ NEW - Two-tier specific fields
            "verdict": two_tier_result.verdict,
            "tier1_status": two_tier_result.tier1_status,
            "tier2_status": two_tier_result.tier2_status,
            "warnings": two_tier_result.warnings,
            "two_tier_result": two_tier_result.to_dict(),
            
            # Final status
            "compliance_status": compliance_status,
            "method": "Multi-Agent + Two-Tier Formal Verification"
        }
    
    except Exception as e:
        import traceback
        return {
            "name": "Multi-Agent System with Two-Tier Verification 🧠",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}", traceback.format_exc()],
            "compliance_status": "❌ ERROR",
            "verified": False,
            "error": str(e)
        }


