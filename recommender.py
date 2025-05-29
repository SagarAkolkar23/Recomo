import os
import re
import json
import requests

def get_recommendations(preference):
    prompt = f"""
Based on the following user preferences, recommend 3 movies. 
For each movie, provide the following details in a structured JSON format:

- name: Movie title
- duration: Duration in minutes
- rating: IMDb or general rating
- poster_url: A link to the movie's poster
- description: A brief description of the movie
- genre: Type or genre of the movie
- cast: Main cast members
- watch_platforms: Platforms where the movie can be streamed (e.g., Netflix, Prime Video)
- watch_links: Direct URLs where the movie can be streamed (if available)

User Preferences: {preference}
Respond ONLY in pure JSON format without any explanation.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini API raw response text:", repr(text))
        print("Gemini API full response:", result)

        # Clean markdown json blocks if any
        cleaned_text = re.sub(r"^```json\s*|\s*```$", "", text.strip())

        movies = json.loads(cleaned_text)
        return movies
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

def get_books_list(preference):
    prompt = f"""
Based on the following user preferences, recommend 3 books.
For each book, provide the following details in a structured JSON format:

- title: Title of the book
- author: Author's name
- genre: Genre or category of the book
- description: A brief summary of the book
- cover_url: A link to the book cover image
- purchase_links: A dictionary of platforms (e.g., Amazon, Goodreads, Google Books) and their direct links

User Preferences: {preference}
Respond ONLY in pure JSON format without any explanation.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]

        # Clean JSON markdown block if present
        cleaned_text = re.sub(r"^```json\s*|\s*```$", "", text.strip())

        books = json.loads(cleaned_text)
        return books
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []
