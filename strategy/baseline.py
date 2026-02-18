from anthropic import Anthropic
from utils.utils import analyze_compliance_answer

def experiment_baseline(query: str, client: Anthropic) -> dict:
    """
    Enhanced Baseline with verdict analysis
    """
    import time
    
    start = time.time()
    steps = ["📝 Direct LLM call without external knowledge"]
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""You are a HIPAA compliance expert. Answer this question:

{query}

Provide a clear, direct answer with:
1. YES or NO at the start
2. Brief explanation
3. Key HIPAA requirements if applicable

Be concise but complete."""
            }]
        )
        
        answer = message.content[0].text
        steps.append("✅ LLM response generated")
        
        # Analyze the answer WITH the question for context
        analysis = analyze_compliance_answer(answer, query)
        steps.append(f"✅ Answer analyzed: {analysis['reasoning']}")
        
        # Determine compliance status
        if analysis['verdict'] == 'compliant':
            compliance_status = "✅ COMPLIANT (based on answer)"
            verified = True
        elif analysis['verdict'] == 'violation':
            compliance_status = "❌ VIOLATION (based on answer)"
            verified = False
        elif analysis['verdict'] == 'conditional':
            compliance_status = "⚠️ CONDITIONAL COMPLIANCE"
            verified = True  # Technically compliant if conditions are met
        else:
            compliance_status = "⚠️ UNKNOWN"
            verified = False
        
        return {
            "name": "Baseline",
            "answer": answer,
            "duration": time.time() - start,
            "steps": steps,
            "method": "Direct LLM (No external knowledge)",
            "compliance_status": compliance_status,
            "verified": verified,
            "analysis": analysis
        }
    
    except Exception as e:
        return {
            "name": "Baseline",
            "answer": f"Error: {str(e)}",
            "duration": time.time() - start,
            "steps": steps + [f"❌ Error: {str(e)}"],
            "method": "Direct LLM (Failed)",
            "compliance_status": "❌ ERROR",
            "verified": False
        }

