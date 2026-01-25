from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = None
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)

def generate_incident_report(error_logs: list[str]) -> str:
    """
    Summarizes a list of raw error logs into a human-readable incident report.
    """
    if not client:
        return "AI Service Unavailable: Missing OpenAI API Key."
        
    if not error_logs:
        return "No errors to analyze. System is healthy."

    # Construct the Prompt
    logs_text = "\n".join(error_logs[:50]) 
    
    prompt = f"""
    You are a Site Reliability Engineer (SRE). 
    Analyze the following raw API error logs:
    
    {logs_text}
    
    Generate a short, tactical Incident Report with:
    1. Summary (What broke?)
    2. Probable Root Cause (Why?)
    3. Recommendations (How to fix?)
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful SRE assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"
