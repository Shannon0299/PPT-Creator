import json
import re
from google.generativeai.types import GenerationConfig
from google.generativeai import GenerativeModel

async def generate_slide_content(model: GenerativeModel, topic: str, num_slides: int, audience: str) -> dict | None:
    """
    Calls the Gemini API to generate structured content for a presentation.

    Args:
        model: The initialized GenerativeModel instance.
        topic: The main topic of the presentation.
        num_slides: The number of content slides (excluding title).
        audience: The target audience for the content.

    Returns:
        A dictionary structured for the PPT builder, or None if generation fails.
    """

    # --- Define the JSON schema for the AI's response ---
    # This is crucial for getting reliable, structured output.
    schema = {
        "type": "OBJECT",
        "properties": {
            "title_slide": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "subtitle": {"type": "STRING"}
                }
            },
            "content_slides": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "title": {"type": "STRING"},
                        "content": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"}
                        }
                    }
                }
            },
            "final_slide": {
                "type": "OBJECT",
                "properties": {
                    "title": {"type": "STRING"},
                    "content": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                }
            }
        },
        "required": ["title_slide", "content_slides", "final_slide"]
    }
    
    # --- Create the prompt for the AI ---
    # We instruct the model to act as an expert and provide a JSON response.
    prompt = f"""
    You are an expert academic content creator. Your task is to generate the content for a PowerPoint presentation.
    
    Topic: "{topic}"
    Target Audience: "{audience}"
    Number of Content Slides: {num_slides}

    Please generate a presentation with:
    1.  A main title slide (title and subtitle).
    2.  Exactly {num_slides} content slides, each with a title and a list of bullet points.
    3.  A final "Thank You" or "Q&A" slide.

    The content should be clear, concise, and tailored for the specified audience.
    Return your response *only* as a JSON object matching the requested schema.
    """

    # --- Configure and call the API ---
    try:
        response = await model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )
        
        # The API returns the JSON as a string in response.text
        # We need to parse it.
        # Sometimes, the model might wrap the JSON in ```json ... ```, so we'll clean it.
        
        cleaned_json = _clean_json_string(response.text)
        
        if not cleaned_json:
            print("Error: AI returned an empty or invalid response.")
            return None
            
        return json.loads(cleaned_json)

    except Exception as e:
        print(f"Error during AI content generation: {e}")
        print(f"Raw response was: {response.text if 'response' in locals() else 'No response'}")
        return None

def _clean_json_string(s: str) -> str:
    """Removes markdown backticks and 'json' prefix from a string."""
    match = re.search(r'```(json)?\s*(\{.*})\s*```', s, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(2)
    return s.strip()
