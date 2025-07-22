import os
import time
import hashlib
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Load environment and API key Chanman
load_dotenv()
os.environ["GROQ_API_KEY"] = "gsk_1XcjxcJEWztqSG4WumeSWGdyb3FYOUrL6BGRF4upWtLn6DiOPYaN"

# Initialize LLM with rate‐limit care
llm = ChatGroq(
    model_name="llama3-8b-8192",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    request_timeout=30,
)

# Build prompt template for translation
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a translation assistant. Translate the user text to English."),
    ("user", "{text}")
])

# Exponential backoff + simple file‐based cache
CACHE_DIR = "translation_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_key(text: str) -> str:
    """Generate a filename-safe hash for caching."""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.txt")

def translate_with_cache(text: str, max_retries=5, base_delay=1.0) -> str:
    """Translate text with caching and exponential backoff on rate limits."""
    key = cache_key(text)
    # Return cached if exists
    if os.path.exists(key):
        with open(key, "r", encoding="utf-8") as f:
            return f.read()

    # Otherwise call the API with exponential backoff
    delay = base_delay
    for attempt in range(1, max_retries + 1):
        try:
            # 1) Build messages list via ChatPromptTemplate
            messages = prompt_template.format_prompt(text=text).to_messages()
            # 2) Invoke the chat model explicitly
            ai_msg = llm.invoke(messages)
            translation = ai_msg.content.strip()
            # Save to cache
            with open(key, "w", encoding="utf-8") as f:
                f.write(translation)
            return translation
        except Exception as e:
            # If rate limit or transient error, back off
            print(f"Attempt {attempt} failed: {e}. Retrying in {delay:.1f}s.")
            time.sleep(delay)
            delay *= 2  # exponential backoff

    # If all retries fail, raise
    raise RuntimeError(f"Translation failed after {max_retries} attempts.")

def translate_dataframe(input_path: str, output_path: str) -> None:
    """Read multilingual Excel, translate all text columns, and write back."""
    df = pd.read_excel(input_path, dtype=str)

    # Translate each cell
    for col in df.columns:
        df[col] = df[col].fillna("").apply(lambda txt: translate_with_cache(txt) if txt else "")

    # Save translated sheet
    df.to_excel(output_path, index=False)

if __name__ == "__main__":
    INPUT_FILE = "Multilingual_Analyst_Assignment.xlsx"
    OUTPUT_FILE = "Multilingual_Analyst_Assignment_translated.xlsx"
    translate_dataframe(INPUT_FILE, OUTPUT_FILE)
    print(f"Translated file saved to {OUTPUT_FILE}")
