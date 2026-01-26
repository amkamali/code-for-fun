import argparse
from pathlib import Path
from PIL import Image
import pytesseract
# import re
import sys

def main():
    """
    Processes an image file to extract text, name, and email using OCR.
    This function accepts an optional image file path as a command-line argument,
    performs optical character recognition (OCR) on the image to extract text,
    searches the extracted text for a name and an email address, and prints the results.
    If no filename is provided, it defaults to 'sample_text_1.jpg'.
    """
    parser = argparse.ArgumentParser(description="Process an image file.")
    parser.add_argument("filename", nargs="?", type=Path, default="sample_text_1.jpg", help="Path to the image file")
    args = parser.parse_args()

    try:
        text = pytesseract.image_to_string(Image.open(args.filename))
    except (FileNotFoundError, OSError) as e:
        print(f"Error: Unable to open image file '{args.filename}': {e}", file=sys.stderr)
        sys.exit(1)

    print("text:", text)
    # TODO: Ignore extraction of name and email for now. Add them in a later PR.
    # name = re.search(r'^[A-Z][a-z]+\s[A-Z][a-z]+', text, re.M)
    # email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    # print("Name:", name.group(0) if name else "-")
    # print("Email:", email.group(0) if email else "-")


if __name__ == '__main__':
    main()
