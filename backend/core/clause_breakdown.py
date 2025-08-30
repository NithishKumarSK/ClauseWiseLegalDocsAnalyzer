import re
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# Initialize Granite LLM client via HuggingFace
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
client = InferenceClient(
    model="ibm-granite/granite-3.3-2b-instruct",
    token=HUGGINGFACE_TOKEN
)

def split_into_clauses(text: str) -> list[str]:
    """
    ClauseWise: Enhanced clause extraction and breakdown
    First tries regex-based detection, then falls back to Granite LLM to
    intelligently split text into clauses if regex fails.
    """

    # --- Regex Clause Extraction (Existing Feature, Kept Untouched) ---
    clause_patterns = [
        r'\n\s*\d+\.\s+',             # Numbered clauses (1. 2. 3.)
        r'\n\s*\([a-z]\)\s+',         # Lettered sub-clauses (a) (b) (c))
        r'\n\s*[A-Z][A-Z\s]+:\s*',    # Section headers (WHEREAS:, THEREFORE:)
        r'\.(?=\s+[A-Z])',            # Sentence boundaries
        r';\s+(?=[A-Z])',             # Semicolon separations
        r'\n\s*\n+',                  # Paragraph breaks
    ]
    
    pattern = '|'.join(f'({p})' for p in clause_patterns)
    clauses = re.split(pattern, text, flags=re.MULTILINE)
    
    cleaned_clauses = []
    for clause in clauses:
        if clause and not re.match(r'^[\s\d\.\(\)a-z]*$', clause):  # Skip separators
            cleaned = clause.strip()
            if len(cleaned) > 20:  # Only include substantial clauses
                cleaned_clauses.append(cleaned)

    # --- Fallback: Simple Regex ---
    if len(cleaned_clauses) < 2:
        simple_clauses = re.split(r"\n\s*\n|;|\.\s+", text)
        cleaned_clauses = [c.strip() for c in simple_clauses if c.strip() and len(c.strip()) > 20]

    # --- AI Fallback (Granite LLM) ---
    if len(cleaned_clauses) < 2 and text.strip():
        try:
            prompt = f"""
            Extract and list the key clauses from the following legal text.
            Return them as a bullet-point list, each clause concise and complete:

            {text}
            """
            response = client.text_generation(prompt, max_new_tokens=800)

            ai_clauses = [c.strip("-• \n") for c in response.split("\n") if len(c.strip()) > 20]

            if ai_clauses:
                cleaned_clauses = ai_clauses

        except Exception as e:
            print("⚠️ AI Clause Extraction Failed:", str(e))

    return cleaned_clauses[:10]  # Limit to 10 for UI performance
