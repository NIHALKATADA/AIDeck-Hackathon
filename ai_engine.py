import os
from groq import Groq
from pydantic import BaseModel
import json

# 1. DATA MODELS (SCHEMA ENFORCEMENT)
class Slide(BaseModel):
    title: str
    bullets: list[str]
    image_prompt: str  # Critical: AI will now generate a visual description per slide

class DataRow(BaseModel):
    column1: str
    column2: str
    column3: str

class AIData(BaseModel):
    presentation: list[Slide]
    dataset: list[DataRow]

# 2. CORE GENERATION LOGIC
def generate_content(topic, num_slides, num_rows, detail, api_key):
    """
    Connects to Groq LPU Cloud to generate structured JSON data.
    Ensures that every slide has text AND a descriptive image prompt.
    """
    client = Groq(api_key=api_key)
    
    # Prompt Engineering: Detailed instructions for the LLM
    prompt = f"""
    You are a professional business consultant. Create a presentation and dataset about '{topic}'.
    
    PRESENTATION:
    - Generate {num_slides} slides.
    - Each slide needs a title and 3-4 professional bullet points.
    - Each slide MUST have an 'image_prompt' field describing a high-quality, professional image 
      (e.g., 'A 3D isometric laboratory with clean blue accents, 4k resolution, professional lighting').
    
    DATASET:
    - Generate {num_rows} rows of sample data with 3 relevant business columns.
    
    Return ONLY a valid JSON object matching this structure exactly:
    {{
      "presentation": [ 
        {{"title": "Slide Title", "bullets": ["Point 1", "Point 2"], "image_prompt": "Image Description"}} 
      ],
      "dataset": [ 
        {{"column1": "Data", "column2": "Data", "column3": "Data"}} 
      ]
    }}
    """

    try:
        # Using Llama 3.3 for high-speed, high-reasoning output
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} # Forces JSON-only response
        )
        
        # Parse and validate the response against our Pydantic model
        raw_json = json.loads(completion.choices[0].message.content)
        return AIData(**raw_json)
        
    except Exception as e:
        # Return the error as a string for the UI to display gracefully
        return str(e)