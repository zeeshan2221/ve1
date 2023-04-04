import requests
import json
import os

# Set up OpenAI API credentials
api_key = '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'
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# Define the input text prompt
text_prompt = "A cat playing piano"

# Define the video settings
video_width = 640
video_height = 640
frame_rate = 30
num_frames = 60

# Define the API endpoint and request payload
endpoint = 'https://api.openai.com/v1/images/generations'
data = {
    'model': 'image-alpha-001',
    'prompt': text_prompt,
    'num_images': 1,
    'size': video_height,
    'response_format': 'url',
    'seed': 42
}

# Generate a list of image URLs
image_urls = []
for i in range(num_frames):
    # Send the request to OpenAI's DALL-E 2 model
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    # Extract the image URL from the response
    image_url = response.json()['data'][0]['url']
    image_urls.append(image_url)

# Define the output video file path
output_video_file = 'output.mp4'

# Define the API endpoint and request payload for encoding the video
endpoint = 'https://api.openai.com/v1/video/generations'
data = {
    'model': 'clip-alpha-001',
    'image_urls': image_urls,
    'fps': frame_rate,
    'response_format': 'url',
    'size': (video_width, video_height),
    'max_length': num_frames,
    'seed': 42
}

# Send the request to OpenAI's CLIP model
response = requests.post(endpoint, headers=headers, data=json.dumps(data))
response.raise_for_status()

# Download the video file from the response URL
video_url = response.json()['data'][0]['url']
response = requests.get(video_url)
response.raise_for_status()
with open(output_video_file, 'wb') as f:
    f.write(response.content)
    
# Display the output video file path
print(f"Video generated: {os.path.abspath(output_video_file)}")
