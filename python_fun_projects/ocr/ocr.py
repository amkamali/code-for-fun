from PIL import Image
import pytesseract, re

text = pytesseract.image_to_string(Image.open('card.jpg'))
name = re.search(r'^[A-Z][a-z]+\s[A-Z][a-z]+', text, re.M)
email = re.search(r'[\w\.-]+@[\w\.-]+', text)
print("Name:", name.group(0) if name else "-")
print("Email:", email.group(0) if email else "-")