import os
import requests
from openai import OpenAI

default_model = "dall-e-2"
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Predefined Styles
STYLES = [
    "realistic photography",
    "cyberpunk futuristic art",
    "anime style",
    "oil painting",
    "pencil sketch",
    "3D render",
    "watercolor painting",
    "fantasy illustration",
    "pixel art"
]


def download_image(url, image_number):
    r = requests.get(url, allow_redirects=True)
    open(f"images/image_{image_number}.png", 'wb').write(r.content)


def generate_images(prompt: str):
    for i, style in enumerate(STYLES):
        print(f"Generating images number {i + 1} with style {style}...")
        finalPrompt = prompt + "with style: " + style
        response = client.images.generate(
            model="dall-e-2",
            prompt=finalPrompt,
            response_format="url",
            quality="standard"
        )
        download_image(response.data[0].url, i + 1)


if __name__ == '__main__':
    prompt = input("Enter a prompt: ")
    if prompt:
        generate_images(prompt)
    else:
        "No prompt entered"
