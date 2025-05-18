import os
import requests
from datetime import datetime

def fetch_apod(api_key):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_image_and_markdown(date, title, explanation, image_url):
    apod_dir = './apod'
    os.makedirs(apod_dir, exist_ok=True)

    image_path = os.path.join(apod_dir, f"{date}.jpg")
    markdown_path = os.path.join(apod_dir, f"{date}.md")

    if not os.path.exists(image_path) and not os.path.exists(markdown_path):
        # Download the image
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as img_file:
            img_file.write(img_data)

        # Create the markdown file
        with open(markdown_path, 'w') as md_file:
            md_file.write(f"---\n")
            md_file.write(f"title: \"{title}\"\n")
            md_file.write(f"date: \"{date}\"\n")
            md_file.write(f"---\n")
            md_file.write(f"{explanation}\n")

def main():
    api_key = os.getenv('NASA_API_KEY')
    if not api_key:
        raise ValueError("NASA_API_KEY environment variable is not set.")

    apod_data = fetch_apod(api_key)
    date = apod_data['date']
    media_type = apod_data['media_type']
    title = apod_data['title']
    explanation = apod_data['explanation']
    image_url = apod_data['url']

    if media_type == "image":
        save_image_and_markdown(date, title, explanation, image_url)

if __name__ == "__main__":
    main()