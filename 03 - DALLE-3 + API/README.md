# Image Generation with OpenAI DALL-E

This project is a Python script for generating images using the OpenAI DALL-E API. The script allows you to input a text prompt, and it generates a specified number of images based on the prompt. The images are saved locally in the `images/` directory.

## Features
- Uses the OpenAI DALL-E API to generate images.
- Accepts a user-provided prompt to customize image generation.
- Downloads and saves generated images as PNG files.

## Prerequisites
To run this script, you need the following:

1. **Python**: Ensure you have Python 3.7 or higher installed.
2. **OpenAI API Key**: Sign up at [OpenAI](https://openai.com/) and generate an API key.
3. **Required Libraries**: Install the following Python libraries:
   - `requests`
   - `openai`

   You can install them using pip:
   ```bash
   pip install requests openai
   ```

## Setup

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/your-repo/image-generator.git
   cd image-generator
   ```

2. **Set Up Environment Variables**:
   Set the `OPENAI_API_KEY` environment variable with your API key. You can do this in your shell or by creating a `.env` file (use a library like `python-dotenv` if needed).
   
   Example for a Unix-based shell:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

3. **Create an `images` Directory**: Ensure there is an `images/` directory in the project root where the generated images will be saved.
   ```bash
   mkdir images
   ```

## Usage

Run the script using the following command:
```bash
python image_generator.py
```

You will be prompted to enter a text description for the images. For example:
```
Enter a prompt: A futuristic cityscape with flying cars at sunset
```
The script will generate 9 images based on your input and save them as `image_1.png`, `image_2.png`, ..., `image_9.png` in the `images/` directory.

## Code Overview

- **Default Model**: The script uses the `dall-e-2` model.
- **Image Download**: The `download_image` function saves images to the local `images/` directory.
- **Image Generation**: The `generate_images` function sends the prompt to the OpenAI API, generates the images, and downloads them.

## Customization

1. **Change Number of Images**:
   Modify the `number_of_images_generated_const` variable to set the number of images to generate.

2. **Save Location**:
   Update the path in the `download_image` function to save images to a different directory.

3. **Quality Settings**:
   Adjust the `quality` parameter in the `generate_images` function if supported by the API.

## Troubleshooting

- **Missing API Key**:
  Ensure the `OPENAI_API_KEY` environment variable is correctly set.

- **Directory Not Found**:
  Make sure the `images/` directory exists before running the script.

- **API Errors**:
  Check your API key validity and usage limits on your OpenAI account dashboard.

## License
This project is licensed under the MIT License. Feel free to use and modify it as needed.

## Acknowledgments
- OpenAI for providing the DALL-E API.
- The Python community for developing the required libraries.

---

Enjoy generating creative images with DALL-E!

