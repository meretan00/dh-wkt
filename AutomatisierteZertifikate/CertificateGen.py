import yaml
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
import fitz  # PyMuPDF


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

workshopid = config["workshopid"]
out_path = workshopid
signaturefile = config["signature"]


participantsdf = pd.read_csv(f"Data\\Workshops\\{workshopid}\\{workshopid}_participants.csv")

participants = pd.Series(participantsdf['Title'].values,
                         index = participantsdf['Name']).to_dict()

with open(f'Data\\Workshops\\{workshopid}\\{workshopid}_description.json',encoding="UTF-8") as description:
    workshop_text = json.load(description)
    print(workshop_text)

if config["language"] is 'de':
    with open(r'Data\de_text.json',encoding="UTF-8") as fixedtext:
        fixed_text = json.load(fixedtext)
        print(fixed_text)
else:
    with open(r'Data\en_text.json',encoding="UTF-8") as fixedtext:
        fixed_text = json.load(fixedtext)
        print(fixed_text)

# Load your background image
background = Image.open(r'Media\WKT_Certificate-01.png')

def draw_multiline_text(draw, text, position, font, color, max_width):
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        # Check if the width of the line with the new word exceeds max_width
        if draw.textsize(test_line, font=font)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # Add the last line

    x, y = position
    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y += font.getsize(line)[1]  # Move to the next line



def add_text_to_image(output_path, fixed_text, workshop_text, participant_name, participant_title):
    # Load the background image
    background = Image.open(r'Media\WKT_Certificate-01.png')
    draw = ImageDraw.Draw(background)

    # Paragraph 2
    if workshop_text["date_begin"] == workshop_text["date_end"]:
        wk_date = datetime.strptime(workshop_text["date_begin"], '%Y-%m-%d').strftime('%d.%m.%Y')
    else:
        wk_date = datetime.strptime(workshop_text["date_begin"], '%Y-%m-%d').strftime('%d.') + '-' + datetime.strptime(workshop_text["date_end"], '%Y-%m-%d').strftime('%d.%m.%Y')
    
    paragraph2_text = f"{fixed_text['sentence2a']} {wk_date} {fixed_text['sentence2b']} {workshop_text['semester']} {fixed_text['sentence2c']}"

    # Color
    #cgreen = (128,128,0)
    cgreen = (83,95,0)

    # Define font and size 
    # Title
    font_size_title = 270
    font_title = ImageFont.truetype("timesbd.ttf", font_size_title)
    # Participant data
    font_size_participant = 75
    font_participant = ImageFont.truetype("timesbd.ttf", font_size_participant)
    # Paragraph 
    font_size_par = 55
    font_par = ImageFont.truetype("times.ttf", font_size_par)
    # Workshop Title
    font_size_wktitle = 75
    font_wktitle = ImageFont.truetype("timesbd.ttf", font_size_wktitle)
    # Contents
    font_size_contentstitle = 55
    font_contentstitle = ImageFont.truetype("timesbd.ttf", font_size_contentstitle)
    # signature
    font_size_sig = 45
    font_sig = ImageFont.truetype("times.ttf", font_size_sig)

    # Place, Date
    # Signature Title
    font_size = 20
    font = ImageFont.truetype("times.ttf", font_size)

    # Example coordinates (adjust these based on your layout)
    title_coords = (200, 850)
    participant_title_coords = (200, 1200)
    participant_coords = (200, 1300)
    paragraph1_coords = (200, 1450)
    coursetitle_coords = (200, 1550)
    paragraph2_coords = (200, 1750)
    contentstitle_coords = (200, 1950)
    placedate_coords = (240,2785)
    sigtitle_coords = (1350,2855)
    sig_placedate_coords = (250,2855)

    

    # Add fixed text
    draw.text(title_coords, fixed_text['title'], fill=cgreen, font=font_title)
    draw.text(participant_title_coords, participant_title, fill="black", font=font_participant)
    draw.text(participant_coords, participant_name, fill="black", font=font_participant)
    draw.text(paragraph1_coords, fixed_text["sentence1"], fill="black", font=font_par)
    draw_multiline_text(draw, workshop_text["course_title"], coursetitle_coords, font_wktitle, cgreen, max_width=2000)
    draw_multiline_text(draw, paragraph2_text, paragraph2_coords, font_par, "black", max_width=2000)
    draw.text(contentstitle_coords, fixed_text["contents"], fill="black", font=font_contentstitle)
    
    
    bullet = u'\u2022'
    ccontents = workshop_text["course_contents"]
    x, y = 250, 2050
    for ccontent in ccontents:
        contenttext = f"{bullet} {ccontent}"
        draw.text((x, y), contenttext, font=font_par, fill="black")
        y += 70  # Adjust for next item
    
    draw.text(placedate_coords, f"{workshop_text['place']}, {datetime.today().strftime('%d.%m.%Y')}", fill="black", font=font_par)
    draw.text(sig_placedate_coords,"Place, Date", fill="black", font=font_sig)
    draw_multiline_text(draw, fixed_text["role"], sigtitle_coords, font_sig, "black", max_width=650)


    # Adding the signature
    png_image_path = fr'Media\{signaturefile}'
    png_img = Image.open(png_image_path)
    # Original dimensions
    original_width, original_height = png_img.size

    # Calculate the new dimensions (80% of the original)
    new_width = int(original_width * 0.65)
    new_height = int(original_height * 0.65)

    # Resize the image
    png_img = png_img.resize((new_width, new_height), Image.ANTIALIAS)

    # Position where you want to paste the png image (top-left corner)
    x, y = 100, 100  # Adjust these values as needed

    # If the PNG image has transparency (alpha channel)
    if png_img.mode in ('RGBA', 'LA') or (png_img.mode == 'P' and 'transparency' in png_img.info):
        # Use alpha composite
        background.paste(png_img, (1250,2650), png_img)

    # Save as PDF
    background.save(output_path, "PDF")

notitle = config["ignoretitles"]

if notitle:
    continue
else:
    notitle = ["nd"]

for key, value in participants.items():
    if value in notitle:
        participanttitle = " "
    else:
        participanttitle = value

    output_path = f"Data/Workshops/{workshopid}/{out_path}/OCR4all_Zertifikat_{key.replace(' ','')}.pdf"

    add_text_to_image(output_path, 
                      fixed_text, 
                      workshop_text, 
                      key, 
                      participanttitle)

