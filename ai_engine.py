import os
from groq import Groq
from pydantic import BaseModel
import json

class Slide(BaseModel):
    title: str
    bullets: list[str]
    # FIX 1: By assigning a default empty string, Pydantic will NEVER crash
    # even if the Streamlit cache forgets to pass this variable.
    image_prompt: str = "" 

class DataRow(BaseModel):
    column1: str
    column2: str
    column3: str

class AIData(BaseModel):
    presentation: list[Slide]
    dataset: list[DataRow]

def generate_content(topic, num_slides, num_rows, detail, api_key):
    client = Groq(api_key=api_key)
    
    # FIX 2: We are giving the AI explicit, strict instructions to NOT rename columns.
    prompt = f"""
    Create a professional presentation and dataset about '{topic}'.
    Presentation: {num_slides} slides. For each slide, provide a title and 3-6 bullets.
    Dataset: {num_rows} rows of sample data with 3 columns.
    
    CRITICAL INSTRUCTION FOR DATASET:
    You MUST use the exact JSON keys "column1", "column2", and "column3". 
    Do NOT invent your own column names based on the topic.
    
    Return ONLY valid JSON matching this exact structure:
    {{
      "presentation": [ {{"title": "Example Title", "bullets": ["Point 1", "Point 2"]}} ],
      "dataset": [ {{"column1": "Data A", "column2": "Data B", "column3": "Data C"}} ]
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