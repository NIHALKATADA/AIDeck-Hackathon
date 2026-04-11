import os
from groq import Groq
from pydantic import BaseModel
import json

class Slide(BaseModel):
    title: str
    bullets: list[str]

class DataRow(BaseModel):
    column1: str
    column2: str
    column3: str

class AIData(BaseModel):
    presentation: list[Slide]
    dataset: list[DataRow]

def generate_content(topic, num_slides, num_rows, detail, api_key):
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Create a professional presentation and dataset about '{topic}'.
    Presentation: {num_slides} slides. For each slide, provide a title and 3-6 bullets.
    Dataset: {num_rows} rows of sample data with 3 columns.
    Return ONLY valid JSON matching this structure:
    {{
      "presentation": [ {{"title": "", "bullets": []}} ],
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