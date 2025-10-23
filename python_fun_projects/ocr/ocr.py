import argparse
from pathlib import Path
from PIL import Image
import pytesseract
import re
import sys

def main():
    parser = argparse.ArgumentParser(description="Process an image file.")
    parser.add_argument("filename", nargs="?", type=Path, default="sample_text_1.jpg", help="Path to the image file")
    args = parser.parse_args()

    try:
        text = pytesseract.image_to_string(Image.open(args.filename))
    except (FileNotFoundError, OSError) as e:
        print(f"Error: Unable to open image file '{args.filename}': {e}", file=sys.stderr)
        sys.exit(1)

    name = re.search(r'^[A-Z][a-z]+\s[A-Z][a-z]+', text, re.M)
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    print("text:", text)
    print("Name:", name.group(0) if name else "-")
    print("Email:", email.group(0) if email else "-")


if __name__ == '__main__':
    main()