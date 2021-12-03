"""
Fetch Aadhar details - Name, DOB, Aadhar No. and Gender from Aadhar image

Install Tesseract - https://github.com/tesseract-ocr/tesseract/wiki/Downloads

install pytesseract - pip install pytesseract
"""

from PIL import Image
import pytesseract
from re import search as re_search
from re import findall as re_findall

# location of the Aadhar image
path = "C:\\Users\\kraa\\Pictures\\Capture.PNG"

img = Image.open(path)
img = img.convert('RGBA')
pix = img.load()

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
            pix[x, y] = (0, 0, 0, 255)
        else:
            pix[x, y] = (255, 255, 255, 255)

# save the processed image temporarily
img.save('temp.png')

# pytesseract to installed location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

raw_result = pytesseract.image_to_string(Image.open('temp.png'))

name = None
dob = None
aadhar_no = None
gender = None

# match name from the text
re_name = "\n.*\n.*\d{2}\/\d{2}\/\d{4}"
res_name = re_findall(re_name, raw_result)
if len(res_name) > 0:
    name = res_name[0].split("\n")[1]

# match dob from the text
re_dob = "\d{2}\/\d{2}\/\d{4}"
res_dob = re_findall(re_dob, raw_result)
if len(res_dob) > 0:
    dob = res_dob[0]

# match aadhar no from the text
re_aadhar_no = "\d{4}.*\d{4}.*\d{4}"
res_aadhar = re_findall(re_aadhar_no, raw_result)
if len(res_aadhar) > 0:
    aadhar_no = res_aadhar[0]

# match gender from the text
re_female = "Female"
re_male = "Male"
gender = re_male if re_search(re_male, raw_result) else gender
gender = re_female if re_search(re_female, raw_result) else gender

# Aadhar details fetched
print("Name       :", name)
print("DOB        :", dob)
print("Aadhar No. :", aadhar_no)
print("Gender     :", gender)
