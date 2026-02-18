
import streamlit as st
import subprocess
import json
import time
from anthropic import Anthropic
import os
from pathlib import Path
import re
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import ast
import PyPDF2
from io import BytesIO
import re
from config import get_precis_path, ARITY_MAP, EXPERIMENTS

PRECIS_PATH = get_precis_path()
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

load_dotenv()
def load_policy_database(csv_path: str = "csv/hipaa_policies_all.csv") -> list:
    try:
        df = pd.read_csv(csv_path)

        policies = []
        for _, row in df.iterrows():

            text = str(row["natural_language"]).lower()

            # very simple keyword extraction (you can improve later)
            auto_keywords = [w.strip(".,;:()") for w in text.split() if len(w) > 4]

            policy = {
                "id": row['policy_id'],
                "section": row['section_number'],
                "title": row['category'],
                "text": row['natural_language'],
                "keywords": auto_keywords,  # <-- FIX
            }

            policies.append(policy)

        print(f"Loaded {len(policies)} policies from CSV.")
        return policies
    except FileNotFoundError:
        st.warning(f"CSV file not found: {csv_path}. Using fallback database.")
        return get_fallback_database()
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return get_fallback_database()

def get_fallback_database() -> list:
    """Fallback policy database if CSV not available"""
    return [
        {
            "id": "HIPAA-164.510b",
            "section": "§164.510(b)",
            "title": "Disclosure to Family Members",
            "text": "A covered entity may disclose protected health information to a family member, other relative, or close personal friend who is involved in the individual's care, with the individual's consent or if the individual is unable to agree.",
            "keywords": ["family", "relatives", "care", "disclosure", "consent", "incapacitated"]
        },
        {
            "id": "HIPAA-164.502a5",
            "section": "§164.502(a)(5)",
            "title": "Business Associate Agreements",
            "text": "A covered entity may disclose protected health information to a business associate if the entity obtains satisfactory assurance that the business associate will appropriately safeguard the information.",
            "keywords": ["business", "associate", "agreement", "contract", "disclosure", "safeguard"]
        },
        {
            "id": "HIPAA-164.506",
            "section": "§164.506",
            "title": "Uses and Disclosures for Treatment, Payment, Healthcare Operations",
            "text": "A covered entity may use or disclose protected health information for treatment, payment, or healthcare operations without individual authorization.",
            "keywords": ["treatment", "payment", "operations", "authorization", "use"]
        },
        {
            "id": "HIPAA-164.512b",
            "section": "§164.512(b)",
            "title": "Public Health Activities",
            "text": "A covered entity may disclose protected health information for public health activities without individual authorization.",
            "keywords": ["public health", "disclosure", "reporting", "disease", "surveillance"]
        },
        {
            "id": "HIPAA-164.530b",
            "section": "§164.530(b)",
            "title": "Privacy Officer Requirement",
            "text": "A covered entity must designate a privacy official who is responsible for the development and implementation of the policies and procedures.",
            "keywords": ["privacy", "officer", "official", "responsibility", "policies"]
        }
    ]

# ============================================
# PRÉCIS INTERFACE
# ============================================

def call_precis_json(formula: str, facts: list) -> dict:
    """
    Call OCaml Précis engine in JSON mode
    
    This is the bridge: Python → OCaml
    """
    
    # Prepare JSON input for OCaml
    request = {
        "formula": formula,
        "facts": {
            "facts": [[pred] + args for pred, *args in facts]
        },
        "regulation": "HIPAA"
    }
    
    try:
        # Call OCaml in JSON mode
        proc = subprocess.Popen(
            [PRECIS_PATH, "json"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=json.dumps(request), timeout=30)
        
        if proc.returncode == 0:
            return {
                "success": True,
                "output": stdout,
                "response": json.loads(stdout) if stdout.strip() else {}
            }
        else:
            return {
                "success": False,
                "error": stderr or "Unknown error"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def analyze_compliance_answer(answer: str, question: str = "") -> dict:
    """
    Intelligently analyze an answer to determine compliance verdict
    Args:
        answer: The LLM's response
        question: The original question (helps with context)
    Returns: {'verdict': 'compliant'|'violation'|'conditional', 'confidence': float, 'reasoning': str}
    """
    
    answer_lower = answer.lower()
    question_lower = question.lower() if question else ""
    
    # Detect question patterns
    is_negative_question = any(word in question_lower for word in [
        'is consent required',
        'is authorization required',
        'must obtain consent',
        'need consent',
        'need authorization'
    ])
    
    is_permission_question = any(phrase in question_lower for phrase in [
        'can', 'may', 'allowed to', 'permitted to'
    ])
    
    is_requirement_question = any(phrase in question_lower for phrase in [
        'must', 'required to', 'shall', 'need to', 'have to'
    ]) and not is_negative_question
    
    # Extract YES/NO
    answer_lines = answer_lower.split('\n')
    first_line = answer_lines[0].strip() if answer_lines else answer_lower
    
    starts_with_yes = first_line.startswith('yes')
    starts_with_no = first_line.startswith('no')
    
    # Also check for yes/no in first few words
    first_words = ' '.join(first_line.split()[:5])
    has_yes = 'yes' in first_words or starts_with_yes
    has_no = 'no' in first_words or starts_with_no
    
    # Decision logic
    if is_negative_question:
        # "Is consent required?" - asking if something restrictive is needed
        if has_no:
            # NO consent required = treatment is ALLOWED = COMPLIANT
            return {
                'verdict': 'compliant',
                'confidence': 0.95,
                'reasoning': 'NO to negative question (consent NOT required) = compliant'
            }
        elif has_yes:
            # YES consent required = more restrictive = COMPLIANT (requirement exists)
            return {
                'verdict': 'compliant',
                'confidence': 0.9,
                'reasoning': 'YES to requirement question = requirement exists'
            }
    
    elif is_permission_question:
        # "Can hospitals share...?"
        if has_yes:
            # Check for conditions
            conditional_words = ['only if', 'provided that', 'must obtain', 'requires authorization']
            has_conditions = any(phrase in answer_lower for phrase in conditional_words)
            
            if has_conditions:
                return {
                    'verdict': 'conditional',
                    'confidence': 0.85,
                    'reasoning': 'YES with conditions to permission question'
                }
            else:
                return {
                    'verdict': 'compliant',
                    'confidence': 0.9,
                    'reasoning': 'YES to permission question = allowed'
                }
        elif has_no:
            return {
                'verdict': 'violation',
                'confidence': 0.9,
                'reasoning': 'NO to permission question = not allowed'
            }
    
    elif is_requirement_question:
        # "Must covered entities have X?"
        if has_yes:
            return {
                'verdict': 'compliant',
                'confidence': 0.9,
                'reasoning': 'YES to requirement = requirement exists'
            }
        elif has_no:
            return {
                'verdict': 'compliant',
                'confidence': 0.85,
                'reasoning': 'NO to requirement = no requirement (compliant by default)'
            }
    
    # Fallback: Look for explicit compliance language
    if any(word in answer_lower for word in ['compliant', 'permitted', 'allowed', 'authorized']):
        return {
            'verdict': 'compliant',
            'confidence': 0.7,
            'reasoning': 'Answer indicates compliance/permission'
        }
    
    if any(word in answer_lower for word in ['violation', 'prohibited', 'not permitted', 'unauthorized']):
        return {
            'verdict': 'violation',
            'confidence': 0.7,
            'reasoning': 'Answer indicates violation/prohibition'
        }
    
    # Unknown
    return {
        'verdict': 'unknown',
        'confidence': 0.3,
        'reasoning': 'Unable to determine clear verdict from answer'
    }


class DocumentExtractor:
    @staticmethod
    def extract_from_pdf(file_bytes) -> str:
        """Extract text from PDF bytes"""
        pdf_file = BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        return text
    
    @staticmethod
    def extract_from_txt(file_bytes) -> str:
        """Extract text from plain text"""
        return file_bytes.decode('utf-8')
    
    @staticmethod
    def extract(uploaded_file) -> str:
        """Auto-detect and extract"""
        file_bytes = uploaded_file.read()
        
        if uploaded_file.name.endswith('.pdf'):
            return DocumentExtractor.extract_from_pdf(file_bytes)
        else:
            return DocumentExtractor.extract_from_txt(file_bytes)

class SectionChunker:
    @staticmethod
    def chunk_by_section_numbers(text: str) -> list:
        """Extract sections based on §XXX.XXX pattern"""
        section_pattern = r'§\s*(\d+\.\d+(?:\([a-z0-9]+\))*)'
        
        sections = []
        matches = list(re.finditer(section_pattern, text))
        
        for i, match in enumerate(matches):
            section_num = match.group(1)
            start = match.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            
            section_text = text[start:end].strip()
            
            # Only include sections with substantial text (>100 chars)
            if len(section_text) > 100:
                sections.append({
                    'section': f"§{section_num}",
                    'text': section_text[:1000]  # Limit to 1000 chars for LLM
                })
        
        return sections

# ============================================
# POLICY PIPELINE
# ============================================

class PolicyIdentifier:
    def __init__(self, client: Anthropic):
        self.client = client
    
    def identify_policies(self, section: dict) -> list:
        """Use LLM to identify policy statements"""
        prompt = f"""Analyze this regulatory text and identify POLICY STATEMENTS.

Text:
{section['text']}

A policy statement specifies:
1. Conditions (IF/WHEN)
2. Actions (MAY/SHALL/MUST)
3. Can be formalized as logic

Output JSON array:
[
  {{
    "statement": "exact text",
    "section": "{section['section']}",
    "title": "brief title",
    "conditions": ["cond1", "cond2"],
    "action": "what is permitted/required"
  }}
]

If no policies, return [].
Output ONLY JSON:"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            if json_match:
                return json.loads(json_match.group())
            return []
        except Exception as e:
            st.error(f"Error identifying policies: {e}")
            return []

class FOTLTranslator:
    def __init__(self, client: Anthropic):
        self.client = client
    
    def translate_policy(self, policy: dict) -> dict:
        """Convert policy to FOTL formula"""
        prompt = f"""Convert this policy to first-order temporal logic (FOTL).

Policy: {policy['statement']}
Section: {policy['section']}
Title: {policy['title']}

FOTL SYNTAX:
- Predicates: coveredEntity(X), protectedHealthInfo(X), disclose(W,X,Y,Z)
- Constants: @Treatment, @Research, @PublicHealth
- Quantifiers: forall X, Y. (...)
- Operators: and, or, implies, not
- Pattern: forall vars. (conditions) implies (action)

EXAMPLES:

Policy: "Covered entity may disclose PHI for treatment without authorization"
FOTL:
forall ce, patient, phi, purpose.
  (coveredEntity(ce) and protectedHealthInfo(phi) and purposeIsPurpose(purpose, @Treatment))
  implies permittedUseOrDisclosure(ce, patient, phi, purpose)

Policy: "Authorization required for research"
FOTL:
forall ce, researcher, phi, purpose.
  (coveredEntity(ce) and protectedHealthInfo(phi) and purposeIsPurpose(purpose, @Research))
  implies requiresAuthorization(ce, researcher, phi)

Output ONLY the FOTL formula:"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            formula = message.content[0].text.strip()
            
            if "```" in formula:
                match = re.search(r'```.*?\n(.*?)\n```', formula, re.DOTALL)
                if match:
                    formula = match.group(1).strip()
            
            # Clean up
            formula = formula.split('\n')[0].strip()
            
            return {
                **policy,
                'fotl_formula': formula
            }
        except Exception as e:
            st.error(f"Error translating policy: {e}")
            return {**policy, 'fotl_formula': 'ERROR'}

class FormulaValidator:
    def __init__(self, precis_path: str):
        self.precis_path = precis_path
    
    def validate(self, formula: str) -> tuple:
        """Validate formula with Précis"""
        wrapped = f"""regulation TEST version "1.0"
policy starts
{formula}
;
policy ends"""
        
        request = {
            "formula": wrapped,
            "facts": {"facts": []},
            "regulation": "TEST"
        }
        
        try:
            proc = subprocess.Popen(
                [self.precis_path, "json"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            
            stdout, stderr = proc.communicate(input=json.dumps(request))
            
            if proc.returncode == 0:
                response = json.loads(stdout)
                if 'error' in response:
                    return False, response['error']
                return True, "Valid"
            else:
                return False, stderr
        except Exception as e:
            return False, str(e)

##====MULTI-POLICY IMPLEMENTATION========##

class RegulationConfig:
    """Configuration for each regulation"""
    
    HIPAA = {
        'name': 'HIPAA',
        'full_name': 'Health Insurance Portability and Accountability Act',
        'section_pattern': r'§\s*(\d+\.\d+(?:\([a-z0-9]+\))*)',
        'section_prefix': '§',
        'predicates': {
            # Entity types (1 arg)
            'coveredEntity': 1,
            'businessAssociate': 1,
            'protectedHealthInfo': 1,
            'publicHealthAuthority': 1,
            # Relationships (2 args)
            'familyMember': 2,
            'involvedInCare': 2,
            'hasRecord': 2,
            'purposeIsPurpose': 2,
            'hasBAA': 2,
            # Permissions (3 args)
            'hasConsent': 3,
            'hasAuthorization': 3,
            # Disclosure (4 args)
            'disclose': 4,
            'permittedUseOrDisclosure': 4,
        },
        'constants': {
            'Treatment', 'Payment', 'HealthcareOperations',
            'Research', 'PublicHealth', 'Emergency'
        },
        'sorts': {'Entity', 'PHI', 'Purpose'},
        'example_formula': """forall ce, patient, phi, purpose.
  (coveredEntity(ce) and protectedHealthInfo(phi) and purposeIsPurpose(purpose, @Treatment))
  implies permittedUseOrDisclosure(ce, patient, phi, purpose)"""
    }
    
    GDPR = {
        'name': 'GDPR',
        'full_name': 'General Data Protection Regulation',
        'section_pattern': r'Article\s+(\d+)',
        'section_prefix': 'Article ',
        'predicates': {
            # Entity types (1 arg)
            'dataSubject': 1,
            'dataController': 1,
            'dataProcessor': 1,
            'personalData': 1,
            'supervisoryAuthority': 1,
            # Relationships (2 args)
            'processingPurpose': 2,
            'hasLegalBasis': 2,
            'purposeIsPurpose': 2,
            # Rights (2 args)
            'hasRight': 2,
            'hasConsent': 2,
            # Processing (3 args)
            'processData': 3,
            'transferData': 3,
            # Adequacy (1 arg)
            'adequacyDecision': 1,
            'appropriateSafeguards': 1,
        },
        'constants': {
            'Consent', 'Contract', 'LegalObligation', 'VitalInterest',
            'PublicInterest', 'LegitimateInterest'
        },
        'sorts': {'Entity', 'PersonalData', 'Purpose', 'LegalBasis'},
        'example_formula': """forall dc, ds, data, purpose.
  (dataController(dc) and dataSubject(ds) and personalData(data) and purposeIsPurpose(purpose, @Consent))
  implies requiresConsent(dc, ds, data)"""
    }
    
    CCPA = {
        'name': 'CCPA',
        'full_name': 'California Consumer Privacy Act',
        'section_pattern': r'Section\s+(\d+(?:\.\d+)?)',
        'section_prefix': 'Section ',
        'predicates': {
            'business': 1,
            'consumer': 1,
            'personalInformation': 1,
            'serviceProvicer': 1,
            'hasOptOut': 2,
            'sellsData': 3,
            'disclosesData': 3,
        },
        'constants': {'Sale', 'Disclosure', 'BusinessPurpose'},
        'sorts': {'Entity', 'PersonalInfo', 'Purpose'},
        'example_formula': """forall b, c, data.
  (business(b) and consumer(c) and personalInformation(data) and sellsData(b, c, data))
  implies hasOptOutRight(c, b)"""
    }
    
    GLBA = {
        'name': 'GLBA',
        'full_name': 'Gramm-Leach-Bliley Act',
        'section_pattern': r'Section\s+(\d+(?:\.\d+)?)',
        'section_prefix': 'Section ',
        'predicates': {
            'financialInstitution': 1,
            'customer': 1,
            'nonpublicPersonalInformation': 1,
            'hasPrivacyNotice': 2,
            'sharesData': 3,
            'optOutProvided': 2,
        },
        'constants': {'Marketing', 'ServiceProvision', 'LegalCompliance'},
        'sorts': {'Entity', 'NonpublicInfo', 'Purpose'},
        'example_formula': """forall fi, cust, info.
  (financialInstitution(fi) and customer(cust) and nonpublicPersonalInformation(info) and sharesData(fi, cust, info))
  implies optOutProvided(cust, fi)"""
    }
    
    SOX = {
        'name': 'SOX',
        'full_name': 'Sarbanes-Oxley Act',
        'section_pattern': r'Section\s+(\d+(?:\.\d+)?)',
        'section_prefix': 'Section ',
        'predicates': {
            'publicCompany': 1,
            'officer': 1,
            'financialReport': 1,
            'hasInternalControls': 2,
            'certifiesReport': 2,
        },
        'constants': {'Accuracy', 'Timeliness', 'Compliance'},
        'sorts': {'Entity', 'Report', 'Purpose'},
        'example_formula': """forall pc, off, report.
  (publicCompany(pc) and officer(off) and financialReport(report) and certifiesReport(off, report))
  implies hasInternalControls(pc, report)"""
    }
    
    COPPA = {
        'name': 'COPPA',
        'full_name': 'Children\'s Online Privacy Protection Act',
        'section_pattern': r'Section\s+(\d+(?:\.\d+)?)',
        'section_prefix': 'Section ',
        'predicates': {
            'operator': 1,
            'child': 1,
            'personalInformation': 1,
            'hasParentalConsent': 2,
            'collectsData': 3,
        },
        'constants': {'ParentalConsent', 'ServiceProvision', 'LegalCompliance'},
        'sorts': {'Entity', 'PersonalInfo', 'Purpose'},
        'example_formula': """forall op, ch, info.
  (operator(op) and child(ch) and personalInformation(info) and collectsData(op, ch, info))
  implies hasParentalConsent(ch, op)"""
    }
    
    
    
    @classmethod
    def get_config(cls, regulation: str):
        """Get configuration for regulation"""
        configs = {
            'HIPAA': cls.HIPAA,
            'GDPR': cls.GDPR,
            'CCPA': cls.CCPA,
            'GLBA': cls.GLBA,
            'SOX': cls.SOX,
            'COPPA': cls.COPPA
        }
        return configs.get(regulation.upper(), cls.HIPAA)
    
    @classmethod
    def detect_regulation(cls, text: str) -> str:
        """Auto-detect regulation from document"""
        text_sample = text[:10000].lower()
        
        scores = {
            'HIPAA': 0,
            'GDPR': 0,
            'CCPA': 0,
            'GLBA': 0,
            'SOX': 0,
            'COPPA': 0
        }
        
        # HIPAA indicators
        if 'health insurance portability' in text_sample or '§164' in text[:5000]:
            scores['HIPAA'] += 10
        if 'covered entity' in text_sample:
            scores['HIPAA'] += 5
        if 'protected health information' in text_sample:
            scores['HIPAA'] += 5
            
        # GDPR indicators
        if 'general data protection regulation' in text_sample:
            scores['GDPR'] += 10
        if re.search(r'article\s+\d+', text[:5000], re.IGNORECASE):
            scores['GDPR'] += 5
        if 'data controller' in text_sample or 'data subject' in text_sample:
            scores['GDPR'] += 5
            
        # CCPA indicators
        if 'california consumer privacy' in text_sample:
            scores['CCPA'] += 10
        if 'section 1798' in text_sample:
            scores['CCPA'] += 5
        
        # GLBA indicators
        if 'gramm-leach-bliley' in text_sample or 'financial institutions' in text_sample:
            scores['GLBA'] += 10
        if 'nonpublic personal information' in text_sample:
            scores['GLBA'] += 5 
        if 'privacy notice' in text_sample:
            scores['GLBA'] += 5

        # SOX indicators
        if 'sarbanes-oxley' in text_sample or 'public company accounting' in text_sample:
            scores['SOX'] += 10
        if 'financial report' in text_sample:
            scores['SOX'] += 5
        if 'internal controls' in text_sample:
            scores['SOX'] += 5  

        # COPPA indicators
        if "children's online privacy" in text_sample or 'section 1303' in text_sample:
            scores['COPPA'] += 10
        if 'parental consent' in text_sample:
            scores['COPPA'] += 5
        if 'personal information of children' in text_sample:
            scores['COPPA'] += 5  
        
        # Determine highest score
        detected = max(scores, key=scores.get)
        return detected if scores[detected] > 0 else 'UNKNOWN'

class TypeSystemGenerator:
    """Auto-generate type system in YOUR format"""
    
    @staticmethod
    def extract_predicates_from_formula(formula: str) -> dict:
        """Extract predicates and their arities from a formula"""
        predicates = {}
        
        # Pattern: predicate_name(arg1, arg2, ...)
        pattern = r'(\w+)\(((?:\w+(?:,\s*)?)+)\)'
        
        for match in re.finditer(pattern, formula):
            pred_name = match.group(1)
            args = [a.strip() for a in match.group(2).split(',')]
            arity = len(args)
            
            # Skip logical operators and keywords
            if pred_name.lower() in ['forall', 'exists', 'and', 'or', 'implies', 'not']:
                continue
                
            predicates[pred_name] = arity
        
        return predicates
    
    @staticmethod
    def extract_constants_from_formula(formula: str) -> set:
        """Extract constants (@Constant) from formula"""
        constants = set()
        pattern = r'@(\w+)'
        
        for match in re.finditer(pattern, formula):
            constants.add(match.group(1))
        
        return constants
    
    @staticmethod
    def generate_type_system(
        regulation: str,
        formulas: list,
        config: dict
    ) -> str:
        """Generate type system in YOUR actual format"""
        
        # Collect all predicates and constants
        all_predicates = {}
        all_constants = set()
        
        for formula in formulas:
            preds = TypeSystemGenerator.extract_predicates_from_formula(formula)
            all_predicates.update(preds)
            
            consts = TypeSystemGenerator.extract_constants_from_formula(formula)
            all_constants.update(consts)
        
        # Build type system file in YOUR format
        lines = []
        lines.append(f"# AUTO-GENERATED TYPE SYSTEM FOR {regulation}")
        lines.append(f"# Generated: {datetime.now().isoformat()}")
        lines.append("")
        
        # PREDICATES section
        lines.append("PREDICATES")
        
        # Add True/False (standard)
        lines.append("True : Bool")
        lines.append("False : Bool")
        
        # Add extracted predicates
        for pred_name, arity in sorted(all_predicates.items()):
            # Generate signature based on arity
            if arity == 1:
                sig = "Entity -> Bool"
            elif arity == 2:
                sig = "Entity Entity -> Bool"
            elif arity == 3:
                sig = "Entity Entity Entity -> Bool"
            elif arity == 4:
                sig = "Entity Entity PHI Purpose -> Bool"
            else:
                sig = " ".join(["Entity"] * arity) + " -> Bool"
            
            lines.append(f"{pred_name} : {sig}")
        
        lines.append("")
        
        # CONSTANTS section
        lines.append("CONSTANTS")
        for const in sorted(all_constants):
            # Infer type - assume Purpose for now
            lines.append(f"@{const} : Purpose")
        
        lines.append("")
        
        # FUNCTIONS section (empty but include structure)
        lines.append("FUNCTIONS")
        lines.append("# Add custom functions here if needed")
        lines.append("# Example: age : Entity -> Int")
        
        return "\n".join(lines)

# ============================================
# POLICY FILE GENERATOR
# ============================================

class PolicyFileGenerator:
    """Generate regulation-specific .policy files"""
    
    @staticmethod
    def generate(
        regulation: str,
        version: str,
        policies: list,
        output_path: str
    ):
        """Generate .policy file"""
        lines = []
        
        # Header
        lines.append(f'regulation {regulation} version "{version}"')
        lines.append("")
        lines.append("policy starts")
        lines.append("")
        
        # Policies
        for policy in policies:
            # Annotation
            annotation = f'@["{policy["section"]} - {policy["title"]}"]'
            lines.append(annotation)
            
            # Formula (ensure proper formatting)
            formula = policy['fotl_formula'].strip()
            if not formula.endswith(';'):
                formula += ' ;'
            
            lines.append(formula)
            lines.append("")
        
        lines.append("policy ends")
        
        # Write file
        content = '\n'.join(lines)
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return content

# ============================================
# MULTI-REGULATION DOCUMENT PIPELINE
# ============================================

class MultiRegulationPipeline:
    """Complete pipeline with auto-generation"""
    
    def __init__(self, client: Anthropic, precis_path: str):
        self.client = client
        self.precis_path = precis_path
    
    def process_document(
        self,
        uploaded_file,
        max_sections: int = 5
    ) -> dict:
        """Process document and generate both policy file and type system"""
        
        results = {
            'regulation': None,
            'sections': [],
            'policies': [],
            'type_system': '',
            'policy_file': '',
            'errors': []
        }
        
        # Step 1: Extract text
        from io import BytesIO
        import PyPDF2
        
        file_bytes = uploaded_file.read()
        
        if uploaded_file.name.endswith('.pdf'):
            pdf_file = BytesIO(file_bytes)
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
        else:
            text = file_bytes.decode('utf-8')
        
        # Step 2: Detect regulation
        regulation = RegulationConfig.detect_regulation(text)
        results['regulation'] = regulation
        
        config = RegulationConfig.get_config(regulation)
        
        # Step 3: Extract sections
        sections = self._extract_sections(text, config, max_sections)
        results['sections'] = sections
        
        # Step 4: Identify policies
        policies = []
        for section in sections:
            section_policies = self._identify_policies(section, regulation)
            policies.extend(section_policies)
        
        # Step 5: Translate to FOTL
        translated_policies = []
        for policy in policies:
            translated = self._translate_policy(policy, config)
            if translated and len(translated.get('fotl_formula', '')) > 20:
                translated_policies.append(translated)
        
        results['policies'] = translated_policies
        
        # Step 6: Generate type system
        formulas = [p['fotl_formula'] for p in translated_policies]
        type_system = TypeSystemGenerator.generate_type_system(
            regulation,
            formulas,
            config
        )
        results['type_system'] = type_system
        
        # Step 7: Generate policy file
        policy_file = PolicyFileGenerator.generate(
            regulation,
            "1.0",
            translated_policies,
            f"policies/{regulation.lower()}_generated.policy"
        )
        results['policy_file'] = policy_file
        
        return results
    
    def _extract_sections(self, text: str, config: dict, max_sections: int) -> list:
        """Extract sections using regulation-specific pattern"""
        sections = []
        pattern = config['section_pattern']
        prefix = config['section_prefix']
        
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        
        for i, match in enumerate(matches[:max_sections]):
            section_num = match.group(1)
            start = match.start()
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            
            section_text = text[start:end].strip()[:2000]
            
            if len(section_text) > 100:
                sections.append({
                    'section': f"{prefix}{section_num}",
                    'text': section_text
                })
        
        return sections
    
    def _identify_policies(self, section: dict, regulation: str) -> list:
        """Identify policy statements in section"""
        prompt = f"""Analyze this {regulation} regulatory text and identify POLICY STATEMENTS.

Text:
{section['text']}

A policy statement specifies conditions and actions that can be formalized.

Output JSON array:
[
  {{
    "statement": "exact text of requirement",
    "section": "{section['section']}",
    "title": "brief title",
    "conditions": ["condition1", "condition2"],
    "action": "what is required/permitted"
  }}
]

If no clear policies, return [].
Output ONLY JSON:"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            
            if json_match:
                policies = json.loads(json_match.group())
                # Filter quality
                return [p for p in policies 
                       if len(p.get('statement', '')) > 50 
                       and p.get('conditions') 
                       and p.get('action')]
            return []
        except:
            return []
    
    def _translate_policy(self, policy: dict, config: dict) -> dict:
        """Translate policy to FOTL"""
        prompt = f"""Convert this {config['name']} policy to first-order logic (FOTL).

Policy: {policy['statement']}
Section: {policy['section']}

AVAILABLE PREDICATES:
{', '.join([f"{p}({a} args)" for p, a in config['predicates'].items()])}

CONSTANTS:
{', '.join([f"@{c}" for c in config['constants']])}

EXAMPLE:
{config['example_formula']}

CRITICAL:
1. Output a COMPLETE formula with both sides of implies
2. Use purposeIsPurpose(var, @Constant) for purposes
3. Formula must end with closing parenthesis
4. Single line output

Output ONLY the formula:"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            formula = message.content[0].text.strip()
            
            # Clean up
            if "```" in formula:
                formula = re.sub(r'```(?:ocaml|fotl)?\s*\n(.*?)\n```', r'\1', formula, flags=re.DOTALL)
                formula = re.sub(r'```', '', formula)
            
            formula = ' '.join(formula.split())
            
            if len(formula) > 20:
                return {**policy, 'fotl_formula': formula}
            
        except Exception as e:
            pass
        
        return None

