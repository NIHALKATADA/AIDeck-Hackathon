import os
from groq import Groq
from pydantic import BaseModel, Field
from typing import List
import json

# --- DATA MODELS ---
class Slide(BaseModel):
    title: str
    bullets: List[str]

class DataRow(BaseModel):
    feature: str
    description: str
    metric: str

class ProjectData(BaseModel):
    presentation: List[Slide]
    dataset: List[DataRow]

def generate_content(topic, num_slides, num_rows, detail_level, api_key):
    client = Groq(api_key=api_key)

    # 1. Define Persona & Rules (Perfectly balanced for all 3 levels)
    if detail_level == "Concise":
        persona = "You are a minimalist copywriter. You write in ultra-short fragments."
        rules = "MANDATORY: Max 2 bullets per slide. Limit to 3-5 words per bullet. Example: 'Launch in 2024.', 'Four crew members.'"
    elif detail_level == "Detailed":
        persona = "You are a technical subject matter expert."
        rules = """
        MANDATORY: Exactly 3 or 4 bullets per slide. 
        STRICT REQUIREMENT: Every single bullet MUST be a full, complete sentence between 15 and 25 words long. 
        Do not use short fragments. 
        Example: 'The Orion spacecraft will utilize a sophisticated life support system capable of sustaining the four-person crew for the duration of the 21-day lunar mission.'
        """
    else: # Standard
        persona = "You are a professional presentation writer."
        rules = """
        MANDATORY: Exactly 3 bullets per slide. 
        STRICT REQUIREMENT: Every single bullet MUST be a complete sentence between 10 and 15 words long. 
        Do not use short fragments.
        Example: 'The Artemis 2 mission will test the Space Launch System and Orion spacecraft capabilities.'
        """

    # 2. System Message strictly handles JSON format
    sys_msg = f"""
    {persona}
    You MUST return ONLY a raw JSON object. No markdown, no intro text.
    SCHEMA:
    {{
        "presentation": [
            {{ "title": "string", "bullets": ["string", "string"] }}
        ],
        "dataset": [
            {{ "feature": "string", "description": "string", "metric": "string" }}
        ]
    }}
    CRITICAL: Use ONLY the keys "presentation" and "dataset". Do not add any other top-level keys.
    """

    # 3. User Message strictly handles the task and constraints
    user_msg = f"""
    Topic: {topic}
    Slides required: {num_slides}
    Rows required: {num_rows}

    CRITICAL RULES YOU MUST OBEY:
    {rules}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg}
            ],
            response_format={"type": "json_object"},
            temperature=0.7, 
        )
        
        raw_json = json.loads(completion.choices[0].message.content)
        
        # Unwrapping logic in case the AI nests the data
        if "presentation" not in raw_json:
            first_key = list(raw_json.keys())[0]
            if isinstance(raw_json[first_key], dict) and "presentation" in raw_json[first_key]:
                raw_json = raw_json[first_key]

        return ProjectData(**raw_json)
    except Exception as e:
        return f"Structure Error: {str(e)}"