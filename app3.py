import os
import pandas as pd
import logging
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from tenacity import retry, wait_exponential, stop_after_attempt
import json
from datetime import datetime
import time
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('property_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

os.environ["GROQ_API_KEY"] = "gsk_1XcjxcJEWztqSG4WumeSWGdyb3FYOUrL6BGRF4upWtLn6DiOPYaN"

# Initialize Groq with conservative settings for free tier
chat = ChatGroq(
    model_name="llama3-8b-8192",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    request_timeout=30,
)

prompt_template = """
Given the following property description, extract these attributes (if present) as a VALID JSON object:
- Project Name
- Carpet Area (in sq meters or sq feet, specify units)
- Built-up Area (specify units)
- Saleable Area (specify units)
- Balcony Area (specify units)
- Terrace Area (specify units)

IMPORTANT: Return ONLY a valid JSON object with these fields. Do not include any additional text or explanation.

Description: {description}
"""

def extract_json_from_response(response_text):
    """Try to extract JSON from a response that might contain extra text"""
    try:
        # First try to parse directly
        return json.loads(response_text)
    except json.JSONDecodeError:
        # If that fails, try to find JSON in the text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
    return None

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(3))
def extract_fields(description):
    try:
        prompt = ChatPromptTemplate.from_template(prompt_template).format(description=description)
        response = chat.invoke(prompt)
        
        # Try to parse the response as JSON
        result = extract_json_from_response(response.content)
        
        if result is None:
            logger.warning(f"Failed to extract JSON from response: {response.content[:200]}...")
            return {"error": "Invalid JSON response", "raw_response": response.content[:500]}
        
        logger.info(f"Successfully processed description (length: {len(description)} chars)")
        return result
        
    except Exception as e:
        logger.error(f"Error processing description: {str(e)}")
        raise

def process_batch(descriptions, batch_size=5, delay_seconds=10):
    """Process descriptions in batches with delays to avoid rate limiting"""
    results = []
    for i in range(0, len(descriptions), batch_size):
        batch = descriptions[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} of {len(descriptions)//batch_size + 1}")
        
        for desc in batch:
            try:
                data = extract_fields(desc)
                results.append(data)
            except Exception as e:
                results.append({"error": str(e)})
                logger.warning(f"Failed to process one item in batch: {e}")
        
        if i + batch_size < len(descriptions):
            logger.info(f"Waiting {delay_seconds} seconds to avoid rate limiting...")
            time.sleep(delay_seconds)
    
    return results

def main():
    try:
        logger.info("Starting property data extraction process")
        start_time = datetime.now()
        
        logger.info("Loading input CSV file")
        df = pd.read_csv("translated_to_english.csv")
        descriptions = df["Property Description"].tolist()
        logger.info(f"Loaded {len(descriptions)} property descriptions")
        
        results = process_batch(descriptions)
        
        output_file = "extracted_properties.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {output_file}")
        
        duration = datetime.now() - start_time
        logger.info(f"Process completed in {duration.total_seconds():.2f} seconds")
        
    except Exception as e:
        logger.error(f"Fatal error in main process: {e}")
        raise

if __name__ == "__main__":
    main()