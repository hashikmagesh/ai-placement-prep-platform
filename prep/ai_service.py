import requests
from django.conf import settings
import pdfplumber

    #Roadmap

def generate_roadmap(domain, company, timeline="3 months"):
    """
    Generate a structured placement preparation roadmap using AI.

    Args:
        domain (str): The target domain/field.
        company (str): The target company.
        timeline (str): Preparation timeline (e.g., "1 month", "3 months", "6 months").

    Returns:
        str: AI-generated roadmap or error message.
    """
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    # Include the timeline in the prompt
    prompt = f"""
        Create a 3-phase structured roadmap.

        Domain: {domain}
        Company: {company}
        Timeline: {timeline}

        Format EXACTLY like this:

        PHASE 1: FOUNDATION
        - bullet
        - bullet

        PHASE 2: SKILLS BUILDING
        - bullet
        - bullet

        PHASE 3: INTERVIEW PREPARATION
        - bullet
        - bullet

        Make it clean and well structured.
    """

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"
    

    #Ask AI
    
def chat_with_ai(user_message):
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""
    You are an AI Placement Assistant.

    Answer the following student question in a helpful and professional way:

    Question: {user_message}
    """

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"
    

    #Questions for Practices

import json
import requests
from django.conf import settings


def generate_aptitude_questions(domain, company, count=5):
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""
    Generate {count} aptitude multiple choice questions for:

    Domain: {domain}
    Company: {company}

    Requirements:
    - Return ONLY valid JSON.
    - No markdown.
    - No explanation text.
    - Format exactly like this:

    [
      {{
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Correct option text"
      }}
    ]
    """

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # 🔥 CLEAN RESPONSE
        text = text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print("JSON parsing failed. Raw response:", text)
            return []
    else:
        print("API Error:", response.status_code, response.text)
        return []
    

#coding page

def generate_coding_questions(domain, company, count=5):
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""
    Generate {count} coding interview problems for:

    Domain: {domain}
    Company: {company}

    Requirements:
    - Return ONLY valid JSON.
    - No markdown.
    - No explanation.
    - Each problem must include:
        title
        description
        leetcode_link (real or closest matching problem)

    Format exactly like:

    [
      {{
        "title": "Two Sum",
        "description": "Problem description...",
        "leetcode_link": "https://leetcode.com/problems/two-sum/"
      }}
    ]
    """

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        text = text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print("Coding JSON parsing failed:", text)
            return []
    else:
        print("Coding API Error:", response.status_code, response.text)
        return []
    
    #interview

def generate_interview_questions(domain, company, count=5):
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""
    Generate {count} interview questions with answers for:

    Domain: {domain}
    Company: {company}

    Requirements:
    - Return ONLY valid JSON.
    - No markdown.
    - No explanation text.
    - Format exactly like:

    [
      {{
        "question": "Explain overfitting.",
        "answer": "Overfitting occurs when..."
      }}
    ]
    """

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        text = text.strip()
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            print("Interview JSON parsing failed:", text)
            return []
    else:
        print("Interview API Error:", response.status_code, response.text)
        return []

def extract_resume_text(resume_file):
    """
    Extract text from uploaded PDF resume
    """

    text = ""

    with pdfplumber.open(resume_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def analyze_resume(resume_text, job_description, company):
    api_key = settings.GEMINI_API_KEY

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze the following resume against the job description and company.

Company:
{company}

Job Description:
{job_description}

Resume:
{resume_text}

Return analysis in this format:

ATS SCORE: (0-100)

MISSING KEYWORDS:
- keyword
- keyword

RESUME ERRORS:
- issue
- issue

SUGGESTIONS:
- suggestion
- suggestion
"""

    headers = {"Content-Type": "application/json"}

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"