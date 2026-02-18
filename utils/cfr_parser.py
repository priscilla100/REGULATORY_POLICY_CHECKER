"""
COMPREHENSIVE CFR TITLE 45 PARSER
Extracts ALL of Title 45 - Public Welfare with flexible filtering

Title 45 Structure:
- Subtitle A: Department of Health and Human Services (Parts 1-199)
  - Subchapter A: General Administration (Parts 1-102)
  - Subchapter B: Health Care Access (Parts 140-159)
  - Subchapter C: Administrative Data Standards (Parts 160-169) ⭐ HIPAA
  - Subchapter D: Health Information Technology (Parts 170-179)
  - Subchapter E: Price Transparency (Parts 180-199)

For HIPAA compliance: Focus on Subchapter C (Parts 160, 162, 164)
For future research: Can access all subchapters
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Set
import re
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# CONFIGURATION: DEFINE TITLE 45 STRUCTURE
# ============================================================================

class Subchapter(Enum):
    """Title 45 Subchapters"""
    GENERAL_ADMIN = "A"              # Parts 1-102
    HEALTH_CARE_ACCESS = "B"         # Parts 140-159
    ADMIN_DATA_STANDARDS = "C"       # Parts 160-169 (HIPAA!)
    HEALTH_IT = "D"                  # Parts 170-179
    PRICE_TRANSPARENCY = "E"         # Parts 180-199

@dataclass
class SubchapterInfo:
    """Metadata about each subchapter"""
    letter: str
    name: str
    part_range: tuple
    description: str

SUBCHAPTER_METADATA = {
    Subchapter.GENERAL_ADMIN: SubchapterInfo(
        letter="A",
        name="General Administration",
        part_range=(1, 102),
        description="General administrative procedures for HHS"
    ),
    Subchapter.HEALTH_CARE_ACCESS: SubchapterInfo(
        letter="B",
        name="Requirements Relating to Health Care Access",
        part_range=(140, 159),
        description="Health care access requirements including accessibility standards"
    ),
    Subchapter.ADMIN_DATA_STANDARDS: SubchapterInfo(
        letter="C",
        name="Administrative Data Standards and Related Requirements",
        part_range=(160, 169),
        description="HIPAA Privacy Rule, Security Rule, and Administrative Simplification"
    ),
    Subchapter.HEALTH_IT: SubchapterInfo(
        letter="D",
        name="Health Information Technology",
        part_range=(170, 179),
        description="Health IT standards, certification, and meaningful use"
    ),
    Subchapter.PRICE_TRANSPARENCY: SubchapterInfo(
        letter="E",
        name="Price Transparency",
        part_range=(180, 199),
        description="Price transparency requirements for hospitals and health plans"
    )
}

# HIPAA-specific parts (within Subchapter C)
HIPAA_PARTS = {
    160: "General Administrative Requirements",
    162: "Administrative Requirements (Transactions and Code Sets)",
    164: "Security and Privacy of Health Information"
}

# ============================================================================
# COMPREHENSIVE CFR PARSER
# ============================================================================

class CFRParser:
    """
    Comprehensive parser for CFR Title 45
    
    Can extract:
    - All of Title 45
    - Specific subchapters
    - Specific parts
    - HIPAA-only policies
    """
    
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.tree = None
        self.root = None
        self._load_xml()
    
    def _load_xml(self):
        """Load and parse XML file"""
        try:
            self.tree = ET.parse(self.xml_path)
            self.root = self.tree.getroot()
            print(f"✅ Loaded CFR XML: {self.xml_path}")
        except Exception as e:
            print(f"❌ Error loading XML: {e}")
            raise
    
    def extract_all(self, include_metadata: bool = True) -> List[Dict]:
        """
        Extract ALL policies from Title 45
        
        Args:
            include_metadata: Add subchapter/part metadata to each policy
        
        Returns:
            List of all policies across all subchapters
        """
        print("📊 Extracting ALL Title 45 policies...")
        
        all_policies = []
        policy_counter = 0
        
        # Extract from all subchapters
        for subchapter, info in SUBCHAPTER_METADATA.items():
            print(f"\n📁 Subchapter {info.letter}: {info.name}")
            print(f"   Parts {info.part_range[0]}-{info.part_range[1]}")
            
            subchapter_policies = self._extract_subchapter(
                subchapter, 
                policy_counter,
                include_metadata
            )
            
            all_policies.extend(subchapter_policies)
            policy_counter += len(subchapter_policies)
            
            print(f"   ✅ Extracted {len(subchapter_policies)} policies")
        
        print(f"\n✅ Total: {len(all_policies)} policies from Title 45")
        return all_policies
    
    def extract_subchapter(self, subchapter: Subchapter, 
                          include_metadata: bool = True) -> List[Dict]:
        """
        Extract policies from a specific subchapter
        
        Args:
            subchapter: Which subchapter to extract
            include_metadata: Add metadata to policies
        
        Returns:
            List of policies from that subchapter
        """
        info = SUBCHAPTER_METADATA[subchapter]
        print(f"📁 Extracting Subchapter {info.letter}: {info.name}")
        
        return self._extract_subchapter(subchapter, 0, include_metadata)
    
    def extract_hipaa_only(self, include_metadata: bool = True) -> List[Dict]:
        """
        Extract only HIPAA-related policies (Parts 160, 162, 164)
        
        This is what you'll use for compliance checking
        """
        print("🔒 Extracting HIPAA policies (Parts 160, 162, 164)...")
        
        policies = []
        policy_counter = 0
        
        for part_num in [160, 162, 164]:
            print(f"\n📄 Part {part_num}: {HIPAA_PARTS[part_num]}")
            
            part_policies = self._extract_part(
                str(part_num),
                policy_counter,
                include_metadata
            )
            
            if include_metadata:
                # Add HIPAA-specific metadata
                for p in part_policies:
                    p['is_hipaa'] = True
                    p['hipaa_part_name'] = HIPAA_PARTS[part_num]
            
            policies.extend(part_policies)
            policy_counter += len(part_policies)
            
            print(f"   ✅ Extracted {len(part_policies)} policies")
        
        print(f"\n✅ Total HIPAA policies: {len(policies)}")
        return policies
    
    def extract_parts(self, part_numbers: List[int], 
                     include_metadata: bool = True) -> List[Dict]:
        """
        Extract specific parts by number
        
        Args:
            part_numbers: List of part numbers to extract (e.g., [160, 164])
        
        Returns:
            Policies from those parts
        """
        policies = []
        policy_counter = 0
        
        for part_num in part_numbers:
            part_policies = self._extract_part(
                str(part_num),
                policy_counter,
                include_metadata
            )
            policies.extend(part_policies)
            policy_counter += len(part_policies)
        
        return policies
    
    def _extract_subchapter(self, subchapter: Subchapter, 
                           start_counter: int,
                           include_metadata: bool) -> List[Dict]:
        """Extract all policies from a subchapter"""
        
        info = SUBCHAPTER_METADATA[subchapter]
        policies = []
        policy_counter = start_counter
        
        # Get part range for this subchapter
        start_part, end_part = info.part_range
        
        for part_num in range(start_part, end_part + 1):
            part_policies = self._extract_part(
                str(part_num),
                policy_counter,
                include_metadata
            )
            
            # Add subchapter metadata
            if include_metadata:
                for p in part_policies:
                    p['subchapter'] = info.letter
                    p['subchapter_name'] = info.name
            
            policies.extend(part_policies)
            policy_counter += len(part_policies)
        
        return policies
    
    def _extract_part(self, part_num: str, start_counter: int,
                     include_metadata: bool) -> List[Dict]:
        """Extract all sections from a specific part"""
        
        policies = []
        
        # Find all PART elements with matching N attribute
        parts = self.root.findall(f".//DIV5[@N='{part_num}']")
        
        if not parts:
            return policies
        
        for part in parts:
            # Get part title
            part_head = part.find('.//HEAD')
            part_title = part_head.text.strip() if part_head is not None else f"Part {part_num}"
            
            # Find all sections (DIV8 elements)
            sections = part.findall('.//DIV8')
            
            for i, section in enumerate(sections):
                policy = self._extract_section(
                    section, 
                    part_num, 
                    start_counter + len(policies)
                )
                
                if policy:
                    if include_metadata:
                        policy['part_title'] = part_title
                    policies.append(policy)
        
        return policies
    
    def _extract_section(self, section: ET.Element, part_num: str, 
                        policy_id: int) -> Optional[Dict]:
        """Extract a single section as a policy"""
        
        # Get section number
        section_num = section.get('N', '')
        if not section_num:
            return None
        
        # Get heading
        head = section.find('.//HEAD')
        if head is None or not head.text:
            return None
        
        heading_text = head.text.strip()
        
        # Parse heading (format: "§ 164.502 Title text")
        heading_match = re.match(r'§\s*(\S+)\s+(.+)', heading_text)
        
        if heading_match:
            section_citation = heading_match.group(1)
            title = heading_match.group(2).strip()
        else:
            section_citation = section_num
            title = heading_text
        
        # Extract all paragraph content
        paragraphs = section.findall('.//P')
        content_parts = []
        
        for p in paragraphs:
            p_text = self._get_element_text(p)
            if p_text.strip():
                content_parts.append(p_text.strip())
        
        full_text = '\n\n'.join(content_parts)
        
        if not full_text:
            return None
        
        # Create policy
        policy = {
            "policy_id": f"HIPAA-{policy_id}",
            "section": f"§{section_citation}",
            "title": title,
            "description": title,
            "category": f"Part {part_num}",
            "text": full_text,
            "natural_language": full_text,
            "part": part_num,
            "cfr_section": section_citation,
            "cfr_part": int(part_num) if part_num.isdigit() else None
        }
        
        return policy
    
    def _get_element_text(self, element: ET.Element) -> str:
        """Recursively extract all text from element"""
        
        text_parts = []
        
        if element.text:
            text_parts.append(element.text)
        
        for child in element:
            child_text = self._get_element_text(child)
            if child_text:
                text_parts.append(child_text)
            
            if child.tail:
                text_parts.append(child.tail)
        
        return ' '.join(text_parts)

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def load_all_title45(xml_path: str = "cfr/title45.xml") -> List[Dict]:
    """
    Load ALL policies from Title 45
    
    For comprehensive research access
    """
    parser = CFRParser(xml_path)
    return parser.extract_all()

def load_hipaa_policies(xml_path: str = "cfr/title45.xml") -> List[Dict]:
    """
    Load only HIPAA policies (Parts 160, 162, 164)
    
    This is what you'll use for your compliance checker
    """
    parser = CFRParser(xml_path)
    return parser.extract_hipaa_only()

def load_by_subchapter(subchapter: Subchapter, 
                       xml_path: str = "cfr/title45.xml") -> List[Dict]:
    """
    Load policies from a specific subchapter
    
    Examples:
    - Subchapter.ADMIN_DATA_STANDARDS for HIPAA
    - Subchapter.HEALTH_IT for Health IT standards
    - Subchapter.PRICE_TRANSPARENCY for price transparency
    """
    parser = CFRParser(xml_path)
    return parser.extract_subchapter(subchapter)

def load_custom_parts(part_numbers: List[int],
                     xml_path: str = "cfr/title45.xml") -> List[Dict]:
    """
    Load specific parts by number
    
    Example: load_custom_parts([160, 164, 170])
    """
    parser = CFRParser(xml_path)
    return parser.extract_parts(part_numbers)

# ============================================================================
# POLICY DATABASE LOADER (REPLACES YOUR CURRENT ONE)
# ============================================================================

def load_policy_database(
    mode: str = "hipaa_only",
    xml_path: str = "cfr/title45.xml"
) -> List[Dict]:
    """
    Flexible policy database loader
    
    Args:
        mode: What to load
            - "hipaa_only": Just HIPAA (Parts 160, 162, 164) - DEFAULT
            - "all": All of Title 45
            - "subchapter_c": All of Subchapter C (Admin Data Standards)
            - "health_it": Health IT standards (Subchapter D)
            - "custom": Specify parts via environment variable
        xml_path: Path to CFR XML file
    
    Returns:
        List of policies
    """
    
    try:
        parser = CFRParser(xml_path)
        
        if mode == "hipaa_only":
            return parser.extract_hipaa_only()
        
        elif mode == "all":
            return parser.extract_all()
        
        elif mode == "subchapter_c":
            return parser.extract_subchapter(Subchapter.ADMIN_DATA_STANDARDS)
        
        elif mode == "health_it":
            return parser.extract_subchapter(Subchapter.HEALTH_IT)
        
        elif mode == "price_transparency":
            return parser.extract_subchapter(Subchapter.PRICE_TRANSPARENCY)
        
        else:
            print(f"⚠️ Unknown mode '{mode}', defaulting to HIPAA only")
            return parser.extract_hipaa_only()
    
    except Exception as e:
        print(f"❌ Error loading policies: {e}")
        print("⚠️ Using fallback database")
        return get_fallback_database()

def get_fallback_database() -> List[Dict]:
    """Minimal fallback if XML fails"""
    return [
        {
            "policy_id": "HIPAA-0",
            "section": "§164.502(a)(1)",
            "title": "Standard: Uses and disclosures of protected health information",
            "description": "General rule for permitted uses and disclosures",
            "category": "Part 164",
            "text": "A covered entity may use or disclose protected health information for treatment, payment, and health care operations.",
            "natural_language": "A covered entity may use or disclose protected health information for treatment, payment, and health care operations.",
            "part": "164",
            "cfr_section": "164.502",
            "is_hipaa": True
        }
    ]

# ============================================================================
# STATISTICS & VALIDATION
# ============================================================================

def analyze_title45(xml_path: str = "cfr/title45.xml"):
    """
    Analyze and show statistics for Title 45
    """
    parser = CFRParser(xml_path)
    
    print("\n" + "="*70)
    print("TITLE 45 - PUBLIC WELFARE ANALYSIS")
    print("="*70)
    
    # Extract all
    all_policies = parser.extract_all()
    
    print(f"\n📊 Total Policies: {len(all_policies)}")
    
    # By subchapter
    print("\n📁 By Subchapter:")
    for subchapter, info in SUBCHAPTER_METADATA.items():
        subchapter_policies = [p for p in all_policies 
                              if p.get('subchapter') == info.letter]
        print(f"   {info.letter}. {info.name}: {len(subchapter_policies)} policies")
        print(f"      Parts {info.part_range[0]}-{info.part_range[1]}")
    
    # HIPAA breakdown
    print("\n🔒 HIPAA Policies (Subchapter C):")
    for part_num, part_name in HIPAA_PARTS.items():
        hipaa_part_policies = [p for p in all_policies 
                              if p.get('cfr_part') == part_num]
        print(f"   Part {part_num} ({part_name}): {len(hipaa_part_policies)} policies")
    
    # Sample policies
    print("\n📋 Sample Policies:")
    for p in all_policies[:5]:
        print(f"   {p['policy_id']} - {p['section']}: {p['title'][:60]}...")
    
    return all_policies

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    import sys
    
    xml_path = sys.argv[1] if len(sys.argv) > 1 else "cfr/title45.xml"
    
    print("🧪 Testing CFR Title 45 Parser")
    print("="*70)
    
    # Analyze
    analyze_title45(xml_path)
    
    # Test different modes
    print("\n" + "="*70)
    print("TESTING DIFFERENT LOAD MODES")
    print("="*70)
    
    modes = ["hipaa_only", "all", "subchapter_c"]
    
    for mode in modes:
        print(f"\n📊 Mode: {mode}")
        policies = load_policy_database(mode=mode, xml_path=xml_path)
        print(f"   Loaded: {len(policies)} policies")
        
        if policies:
            print(f"   Sample: {policies[0]['policy_id']} - {policies[0]['section']}")
