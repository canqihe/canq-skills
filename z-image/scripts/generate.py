#!/usr/bin/env python3
"""
ModelScope Image Generation Script
Generates AI images using ModelScope API with async polling
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

# Configuration
BASE_URL = "https://api-inference.modelscope.cn/"
DEFAULT_MODEL = "Tongyi-MAI/Z-Image-Turbo"
DEFAULT_OUTPUT_DIR = Path.home() / "Desktop"


def get_skill_dir():
    """Get the skill directory path"""
    return Path(__file__).parent.parent


def load_config():
    """Load configuration from config.json"""
    config_file = get_skill_dir() / "config.json"

    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)

    return {}


def get_api_key(args):
    """Get API key from various sources with priority"""
    # Priority 1: Command line argument
    if args.api_key:
        return args.api_key

    # Priority 2: Config file
    config = load_config()
    if "api_key" in config and config["api_key"]:
        return config["api_key"]

    # Priority 3: Environment variable
    env_key = os.environ.get("MODELSCOPE_API_KEY")
    if env_key:
        return env_key

    return None


def init_config():
    """Initialize config.json file"""
    config_file = get_skill_dir() / "config.json"

    if config_file.exists():
        print("⚠️  config.json already exists")
        return

    default_config = {
        "api_key": "",
        "default_model": DEFAULT_MODEL,
        "output_dir": DEFAULT_OUTPUT_DIR
    }

    with open(config_file, "w") as f:
        json.dump(default_config, f, indent=2)

    print(f"✅ Config file created: {config_file}")
    print("⚠️  Please edit config.json and add your ModelScope API key")
    print("   Get your API key from: https://modelscope.cn/my/myaccesstoken")


def generate_image(prompt, api_key, model=None, filename=None):
    """Generate an image using ModelScope API"""
    if not api_key:
        print("❌ API key not found!")
        print("   Please set it in config.json or use --api-key argument")
        return None

    if model is None:
        config = load_config()
        model = config.get("default_model", DEFAULT_MODEL)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # Submit generation task
    print(f"🎨 Generating image: {prompt}")
    print(f"📦 Model: {model}")

    try:
        response = requests.post(
            f"{BASE_URL}v1/images/generations",
            headers={**headers, "X-ModelScope-Async-Mode": "true"},
            data=json.dumps({
                "model": model,
                "prompt": prompt
            }, ensure_ascii=False).encode('utf-8')
        )
        response.raise_for_status()
        task_id = response.json()["task_id"]
        print(f"✅ Task submitted: {task_id}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to submit task: {e}")
        return None

    # Poll for completion
    print("⏳ Waiting for image generation...")

    while True:
        try:
            result = requests.get(
                f"{BASE_URL}v1/tasks/{task_id}",
                headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
            )
            result.raise_for_status()
            data = result.json()

            if data["task_status"] == "SUCCEED":
                image_url = data["output_images"][0]
                print(f"✅ Image ready: {image_url}")

                # Download and save image
                return download_and_save_image(image_url, filename)

            elif data["task_status"] == "FAILED":
                print("❌ Image generation failed")
                return None

            time.sleep(5)

        except requests.exceptions.RequestException as e:
            print(f"❌ Error polling task status: {e}")
            return None


def download_and_save_image(url, filename=None):
    """Download image and save to output directory"""
    skill_dir = get_skill_dir()
    config = load_config()
    output_dir = skill_dir / config.get("output_dir", DEFAULT_OUTPUT_DIR)

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"result_image_{timestamp}.jpg"

    output_path = output_dir / filename

    try:
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        image.save(output_path)

        print(f"✅ Image saved: {output_path}")
        return str(output_path)

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download image: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to save image: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Generate images using ModelScope API")
    parser.add_argument("--prompt", default=None, help="Text prompt for image generation")
    parser.add_argument("--model", default=None, help=f"Model ID (default: {DEFAULT_MODEL})")
    parser.add_argument("--filename", default=None, help="Output filename (default: auto-generated)")
    parser.add_argument("--api-key", default=None, help="ModelScope API key")
    parser.add_argument("--setup", action="store_true", help="Initialize config.json")

    args = parser.parse_args()

    # Handle setup mode
    if args.setup:
        init_config()
        return

    # Require prompt for image generation
    if not args.prompt:
        parser.error("--prompt is required unless using --setup")

    # Generate image
    result = generate_image(args.prompt, get_api_key(args), args.model, args.filename)

    if result:
        print(f"\n🎉 Success!")
        print(f"📁 Image saved to: {result}")
    else:
        print("\n❌ Image generation failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
