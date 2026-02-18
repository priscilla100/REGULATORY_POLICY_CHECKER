from pathlib import Path
import os

"""
config.py - Centralized Configuration
This file should be imported by other modules, never import from them
"""

import os

EXPERIMENTS= {
    "baseline_no_context": {
        "exp_name": "Baseline",
        "description": "Direct LLM call with no external knowledge",
        "use_retrieval": False,
        "use_precis": False
    },
    "rag": {
        "exp_name": "RAG",
        "description": "Retrieve natural language policies from database and provide to LLM",
        "use_retrieval": True,
        "use_precis": False
    },
    "pipeline": {
        "exp_name": "Pipeline4Compliance ⭐",
        "description": "Complete pipeline: LLM1 (extract + translate) → OCaml Précis → LLM2 (explain)",
        "use_retrieval": False,
        "use_precis": True
    },
    "agentic": {
       "exp_name": "Agent4Compliance ⭐",
        "description": "Full Agent Reasoning, tool use, replanning using CrewAI",
        "use_retrieval": False,
        "use_precis": True 
    }
}

ARITY_MAP = {
    # Entity type predicates (1 argument)
    'coveredEntity': 1,
    'protectedHealthInfo': 1,
    'publicHealthAuthority': 1,
    
    # Action predicates (4 arguments)
    'disclose': 4,
    'permittedUseOrDisclosure': 4,
    
    # Authorization predicates (3 arguments)
    'hasAuthorization': 3,
    
    # Requirement predicates (1 argument)
    'requiredByLaw': 1,
    
    # Comparison predicates (2 arguments)
    'purposeIsPurpose': 2,
}

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def get_precis_path():
    """
    Automatically find précis executable in any environment
    No hardcoded paths needed!
    """
    
    # Priority 1: Environment variable (for custom deployments)
    if "PRECIS_PATH" in os.environ:
        path = os.environ["PRECIS_PATH"]
        if os.path.exists(path) and os.access(path, os.X_OK):
            return path
    
    # Priority 2: Current working directory (most deployments)
    cwd_path = os.path.join(os.getcwd(), "precis")
    if os.path.exists(cwd_path):
        # Try to make it executable if needed
        if not os.access(cwd_path, os.X_OK):
            try:
                os.chmod(cwd_path, 0o755)
            except:
                pass
        if os.access(cwd_path, os.X_OK):
            return cwd_path
    
    # Priority 3: Relative to this file's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_relative = os.path.join(script_dir, "precis")
    if os.path.exists(script_relative) and os.access(script_relative, os.X_OK):
        return script_relative
    
    # Priority 4: One level up (if this file is in utils/)
    parent_path = os.path.join(script_dir, "..", "precis")
    if os.path.exists(parent_path) and os.access(parent_path, os.X_OK):
        return os.path.abspath(parent_path)
    
    # Priority 5: Common deployment locations
    common_paths = [
        "./precis",
        "/app/precis",  # Heroku/Railway
        "/opt/precis",  # Docker containers
    ]
    
    for path in common_paths:
        if os.path.exists(path) and os.access(path, os.X_OK):
            return os.path.abspath(path)
    
    # Not found
    return None

def get_precis_working_dir():
    """Get the working directory for précis execution"""
    precis_path = get_precis_path()
    if precis_path:
        return os.path.dirname(os.path.abspath(precis_path)) or "."
    return os.getcwd()

PRECIS_CONFIG = {
    "path": get_precis_path(),
    "working_dir": get_precis_working_dir(),
    "timeout": 30
}
def validate_precis_setup():
    """
    Check if précis is properly configured
    Call this on app startup to show clear errors early
    """
    path = PRECIS_CONFIG["path"]
    
    if path is None:
        return {
            "valid": False,
            "error": "Précis executable not found",
            "details": f"Current directory: {os.getcwd()}",
            "suggestion": "Make sure 'precis' file is in your project root directory and run: chmod +x precis",
            "files_in_cwd": os.listdir(os.getcwd())[:20]
        }
    
    if not os.path.exists(path):
        return {
            "valid": False,
            "error": f"Précis path does not exist: {path}",
            "suggestion": "Check file permissions and deployment configuration"
        }
    
    if not os.access(path, os.X_OK):
        return {
            "valid": False,
            "error": f"Précis file is not executable: {path}",
            "suggestion": "Run: chmod +x precis"
        }
    
    return {
        "valid": True,
        "path": path,
        "working_dir": PRECIS_CONFIG["working_dir"],
        "message": "✅ Précis engine ready"
    }
