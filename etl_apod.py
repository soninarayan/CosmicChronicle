import os
import sys
import json
import requests
import argparse
from datetime import datetime, date

def fetch_apod(api_key, date_str=None):
    """Fetch APOD data from NASA API with error handling."""
    url = f"https://api.nasa.gov/planetary/apod"
    params = {
        'api_key': api_key,
        'thumbs': True  # Get video thumbnails if available
    }
    
    if date_str:
        params['date'] = date_str
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"API Response: {json.dumps(data, indent=2)}", file=sys.stderr)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching APOD data: {e}", file=sys.stderr)
        raise

def get_media_info(apod_data):
    """Extract media information from APOD data."""
    media_type = apod_data['media_type']
    media_info = {
        'type': media_type,
        'image_url': None,
        'video_url': None
    }

    if media_type == 'image' and 'url' in apod_data:
        media_info['image_url'] = apod_data['url']
    elif media_type == 'video':
        if 'url' in apod_data:
            media_info['video_url'] = apod_data['url']
        if 'thumbnail_url' in apod_data:
            media_info['image_url'] = apod_data['thumbnail_url']
    else:
        print(f"Note: Unsupported media type '{media_type}'", file=sys.stderr)
        if 'url' in apod_data:
            media_info['video_url'] = apod_data['url']

    return media_info

def save_image_and_markdown(date_str, title, explanation, media_info, copyright_info=None):
    """Save image and create markdown with media information."""
    apod_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apod')
    os.makedirs(apod_dir, exist_ok=True)

    image_path = os.path.join(apod_dir, f"{date_str}.jpg")
    markdown_path = os.path.join(apod_dir, f"{date_str}.md")

    # Skip if both files already exist
    if os.path.exists(markdown_path):
        print(f"Files already exist for {date_str}, skipping", file=sys.stderr)
        return

    # Create markdown first
    with open(markdown_path, 'w') as md_file:
        md_file.write("---\n")
        md_file.write(f'title: "{title}"\n')
        md_file.write(f'date: "{date_str}"\n')
        md_file.write(f'media_type: "{media_info["type"]}"\n')
        if media_info['video_url']:
            md_file.write(f'video_url: "{media_info["video_url"]}"\n')
        if copyright_info:
            md_file.write(f'copyright: "{copyright_info}"\n')
        md_file.write("---\n\n")
        md_file.write(f"{explanation}\n")
        
        # Add media links at the bottom
        if media_info['video_url']:
            md_file.write(f"\n[View Video]({media_info['video_url']})\n")
        if media_info['image_url']:
            md_file.write(f"\n![APOD]({date_str}.jpg)\n")
    
    print(f"Created markdown file {markdown_path}", file=sys.stderr)

    # Download image if available
    if media_info['image_url']:
        try:
            response = requests.get(media_info['image_url'])
            response.raise_for_status()
            with open(image_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f"Downloaded {'thumbnail' if media_info['video_url'] else 'image'} to {image_path}", file=sys.stderr)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}", file=sys.stderr)
            # Don't raise the error - we still created the markdown file successfully

def main():
    """Main function with enhanced error handling."""
    parser = argparse.ArgumentParser(description='Fetch NASA Astronomy Picture of the Day')
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format')
    args = parser.parse_args()

    try:
        api_key = os.getenv('NASA_API_KEY')
        if not api_key:
            raise ValueError("NASA_API_KEY environment variable is not set")

        # Fetch APOD data
        apod_data = fetch_apod(api_key, args.date)
        
        # Extract required fields with error handling
        required_fields = ['date', 'media_type', 'title', 'explanation']
        for field in required_fields:
            if field not in apod_data:
                raise KeyError(f"Missing required field in API response: {field}")

        # Get media information
        media_info = get_media_info(apod_data)

        # Save content
        save_image_and_markdown(
            apod_data['date'],
            apod_data['title'],
            apod_data['explanation'],
            media_info,
            apod_data.get('copyright')
        )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()