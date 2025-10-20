from PIL import Image, ImageDraw, ImageFont
import json
from datetime import datetime
#local
from CertGUI import Certificator
import os
import csv
#local
import input_checker
import sys

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # <- temporärer Pfad im PyInstaller-Bundle
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
   
#Takes list with elements as folders and files that lead to the wanted file.
#Location stands in relation to your py-file (eg. within the same folder the list is simply the file ["202311_ORC4all.json"])
def get_file_path(file_path: list):
    return os.path.join(BASE_DIR, *file_path)

def draw_multiline_text(draw, text, position, font, color, max_width):
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        # Check if the width of the line with the new word exceeds max_width
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # Add the last line

    x, y = position
    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y += font.getlength(line)  # Move to the next line

#Import and edit the Cetificator class
class GUI(Certificator):
    def __init__(self):
        super().__init__()

    def combine_pathes(self, filepath):
        return os.path.join(BASE_DIR, filepath)
    
    def add_text_to_image(self, output_path, fixed_text, participant_name):
        # Load the background image
        background = Image.open(self.combine_pathes(r"Media\\WKT_Certificate-01.png"))
        draw = ImageDraw.Draw(background)

        # Paragraph 2 - Date
        if self.date_end_variable.get() == "":
            self.date_end_variable.set(self.date_start_variable.get())
            
        if self.date_start_variable.get() == self.date_end_variable.get():
            wk_date = datetime.strptime(self.date_start_variable.get(), '%Y-%m-%d').strftime('%d.%m.%Y')
        else:
            wk_date = datetime.strptime(self.date_start_variable.get(), '%Y-%m-%d').strftime('%d.') + '-' + datetime.strptime(self.date_end_variable.get(), '%Y-%m-%d').strftime('%d.%m.%Y')
        
        paragraph2_text = f"{fixed_text['sentence2a']} {wk_date} {fixed_text['sentence2b']}"
        paragraph3_text = f"{fixed_text['sentence2b2']} {fixed_text['sentence2b3']} {self.semester.get()}"
        paragraph4_text = f"{fixed_text['sentence2c']}"
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
        font_size_wktitle = int(self.title_size.get())
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
        paragraph2_coords = (200, 1650)
        paragraph3_coords = (200, 1750)
        paragraph4_coords = (200, 1850)
        contentstitle_coords = (200, 1950)
        placedate_coords = (240,2785)
        sigtitle_coords = (1350,2855)
        sig_placedate_coords = (250,2855)


        # Add fixed text and Workshop title
        draw.text(title_coords, fixed_text['title'], fill=cgreen, font=font_title)
        draw.text(participant_coords, participant_name, fill="black", font=font_participant)
        draw.text(paragraph1_coords, fixed_text["sentence1"], fill="black", font=font_par)
        draw_multiline_text(draw, self.workshop_title_variable.get(), coursetitle_coords, font_wktitle, cgreen, max_width=2000)
        draw_multiline_text(draw, paragraph2_text, paragraph2_coords, font_par, "black", max_width=2500)
        draw_multiline_text(draw, paragraph3_text, paragraph3_coords, font_par, "black", max_width=2500)
        draw_multiline_text(draw, paragraph4_text, paragraph4_coords, font_par, "black", max_width=2500)
        draw.text(contentstitle_coords, fixed_text["contents"], fill="black", font=font_contentstitle)
        
        #Write Workshop Content on certificate
        bullet = u'\u2022'
        x, y = 250, 2050
        for stringvar in self.descr_list:
            if stringvar.get() != "":
                contenttext = f"{bullet} {stringvar.get()}"
            else:
                contenttext = ""
            draw.text((x, y), contenttext, font=font_par, fill="black")
            y += 70  # Adjust for next item
        
        draw.text(placedate_coords, f"Rostock, {datetime.today().strftime('%d.%m.%Y')}", fill="black", font=font_par)
        draw.text(sig_placedate_coords,"Place, Date", fill="black", font=font_sig)
        draw_multiline_text(draw, fixed_text["role"], sigtitle_coords, font_sig, "black", max_width=1000)


        # Adding the signature
        png_img = Image.open(self.signature_variable.get())
        # Original dimensions
        original_width, original_height = png_img.size

        # Calculate the new dimensions (80% of the original)
        new_width = int(original_width * 0.65)
        new_height = int(original_height * 0.65)

        # Resize the image
        png_img = png_img.resize((new_width, new_height), Image.LANCZOS)

        # Position where you want to paste the png image (top-left corner)
        x, y = 100, 100  # Adjust these values as needed

        # If the PNG image (Signature) has transparency (alpha channel)
        if png_img.mode in ('RGBA', 'LA') or (png_img.mode == 'P' and 'transparency' in png_img.info):
            # Use alpha composite
            background.paste(png_img, (1400,2600), png_img)

        # Save as PDF
        background.save(output_path, "PDF")
        

    #Overrite methode to grab all tkinter variables when Button "Create" is pressed
    def create_certificates(self):
        #Read the user chosen participants csv into python and test for specifications
        try:
            with open(self.participant_list_variable.get(), "r", encoding="utf-8-sig") as f:
                csv_file = csv.reader(f)
                #Check if csv has more than one column
                participants =[row for row in csv_file]
                first_row = next(csv_file, None)
                if first_row is not None:
                    if len(first_row) == 1:
                        response_csv = ""
                    else:
                        response_csv = "Teilnehmerliste hat mehr als eine Spalte.\n"
                else:
                    response_csv = "Teilnehmerliste ist leer.\n"

        except FileNotFoundError:
            self.notification_variable.set("Datei der Teilnehmerliste nicht gefunden.\nBitte überprüfen, ob Datei ausgewählt wurde oder vorhanden ist.\n")
            return None
    
        #Reset Notification Label
        self.notification_variable.set("")
        #check input of different instance variables
        response_semester = input_checker.check_semester(self.semester.get())
        response_prefix = input_checker.check_prefix(self.workshopname_variable.get())
        response_start = input_checker.check_time(self.date_start_variable.get())
        response_end = input_checker.check_time(self.date_end_variable.get())
        if self.language_variable.get() == "":
            response_language = "Bitte eine Sprache auswählen.\n"
        else:
            response_language = ""
        if self.folderpath_variable.get() == "":
            response_filepath = "Bitte einen Ablageordner auswählen.\n"
        else:
            response_filepath = ""
        #Fill Notification Label
        self.notification_variable.set(f"{response_semester}{response_prefix}{response_start}{response_end}{response_language}{response_filepath}{response_csv}")


        if self.language_variable.get() == "de":   
            #Load Workshop Description - change later into something interactive
            with open(self.combine_pathes("Data\\de_text.json"),encoding="UTF-8") as fixedtext:
                fixed_text = json.load(fixedtext)
        else:
            with open(self.combine_pathes("Data\\en_text.json"),encoding="UTF-8") as fixedtext:
                fixed_text = json.load(fixedtext)
        
        for name in participants:
            #Put information together with add_text_to_image function
            clear_name = name[0]
            self.add_text_to_image(os.path.join(self.folderpath_variable.get(), f"{self.workshopname_variable.get()}_{name[0]}.pdf"), 
                                    fixed_text, 
                                    #workshop_text, 
                                    clear_name)
            self.notification_variable.set(f"Die Zertifikate wurden erfolgreich erstellt und in {self.folderpath_label_variable.get()} abgelegt.")

gui = GUI()
