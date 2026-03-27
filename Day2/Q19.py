articles = [
    {"title": "AI Intro", "tags": ["python", "ml", "ai"]},
    {"title": "Web Dev", "tags": ["python", "fastapi", "api"]},
    {"title": "Data 101", "tags": ["ml", "pandas", "python"]},
]

unique_tags = sorted({tag for article in articles for tag in article["tags"]})
print(unique_tags)