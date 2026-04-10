import os
from groq import Groq
from pydantic import BaseModel
import json

# Data Models
class Slide(BaseModel):
    title: str
    bullets: list[str]
    image_prompt: str  # AI generates a descriptive prompt for the image

class DataRow(BaseModel):
    column1: str
    column2: str
    column3: str

class AIData(BaseModel):
    presentation: list[Slide]
    dataset: list[DataRow]

def generate_content(topic, num_slides, num_rows, detail, api_key):
    client = Groq(api_key=api_key)
    
    # Updated prompt to explicitly ask for image descriptions
    prompt = f"""
    Create a professional presentation and dataset about '{topic}'.
    Presentation: {num_slides} slides. For each slide, provide a title, 3-4 bullets, 
    and a 'image_prompt' that describes a professional visual (e.g., 'Minimalist 3D icon of a rocket launching, corporate blue style').
    Dataset: {num_rows} rows of sample data with 3 columns.
    Return ONLY valid JSON matching this structure:
    {{
      "presentation": [ {{"title": "", "bullets": [], "image_prompt": ""}} ],
      "dataset": [ {{"column1": "", "column2": "", "column3": ""}} ]
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        return AIData(**data)
    except Exception as e:
        return str(e)