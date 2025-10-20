import tkinter as tk   
from tkinter import ttk
from tkinter import filedialog
import os
import re
import json
import sys
#Local
import input_checker

class Certificator():
    def __init__(self):
        #GUI
        root = tk.Tk()
        root.geometry("750x500")
        
        #Initiate all Variables for Buttons, Labels and Entries
        self.workshopname_variable = tk.StringVar(root)
        self.date_start_variable = tk.StringVar(root)
        self.date_end_variable = tk.StringVar(root)
        self.participant_list_variable = tk.StringVar(root)
        self.participant_list_label_variable = tk.StringVar(root)
        self.folderpath_variable = tk.StringVar(root)
        self.folderpath_label_variable = tk.StringVar(root)
        self.signature_variable = tk.StringVar(root)
        self.signature_label_variable = tk.StringVar(root)
        self.language_variable = tk.StringVar(root)
        #self.description_variable = tk.StringVar(root)
        #self.description_label_variable = tk.StringVar(root)
        self.title_size = tk.StringVar(root)
        self.title_size.set(70)
        self.semester = tk.StringVar(root)
        self.semester.set("Wintersemester 24/25")
        
        #Variables for Descriptions on Certificate
        self.workshop_title_variable = tk.StringVar(root)
        self.workshop_descr_0_variable = tk.StringVar(root)
        self.workshop_descr_1_variable = tk.StringVar(root)
        self.workshop_descr_2_variable = tk.StringVar(root)
        self.workshop_descr_3_variable = tk.StringVar(root)
        self.workshop_descr_4_variable = tk.StringVar(root)
        self.workshop_descr_5_variable = tk.StringVar(root)
        self.workshop_descr_6_variable = tk.StringVar(root)
        self.workshop_descr_7_variable = tk.StringVar(root)
        self.workshop_descr_8_variable = tk.StringVar(root)
        self.workshop_descr_9_variable = tk.StringVar(root)
        self.notification_variable = tk.StringVar(root)
        self.description = {"workshop_title": "", "workshop_content": [ ]}
        #Hopefully temporary list of descr_variables
        self.descr_list = [self.workshop_descr_0_variable, self.workshop_descr_1_variable, self.workshop_descr_2_variable,
                        self.workshop_descr_3_variable, self.workshop_descr_4_variable, self.workshop_descr_5_variable,
                        self.workshop_descr_6_variable, self.workshop_descr_7_variable, self.workshop_descr_8_variable,
                        self.workshop_descr_9_variable]
        # Wenn es als .exe läuft
        if getattr(sys, 'frozen', False):
            self.BASE_DIR = sys._MEIPASS  # temporärer Entpackpfad von PyInstaller
        else:
            # Wenn es als .py läuft
            self.BASE_DIR = os.path.dirname(__file__)

        self.start_path = self.BASE_DIR
        #Set default for signature
        self.signature_variable.set(os.path.join(self.BASE_DIR, "unterschrift.png"))
        
        root.title("Zertifikate der Digitalen Hermeneutik")
        #Label Workshop Information
        label_semester = ttk.Label(root,text="Semester:")
        label_semester.place(x=5, y=5)
        entry_semester = ttk.Entry(root, textvariable=self.semester)
        entry_semester.place(x=150, y=5)
        

        #Entry Workshop name
        label_workshopname = ttk.Label(root, text = "Filepräfix: \nYYYYMMDD_title")
        label_workshopname.place(x=5, y=30)
        entry_workshopname = ttk.Entry(root, textvariable = self.workshopname_variable)
        entry_workshopname.place(x=150, y=30)
        #Entry Workshop Starting Date
        label_date_start = ttk.Label(root, text = "Workshopbeginn in der\nForm 2023-11-23")
        label_date_start.place(x=5, y= 70)
        entry_date_start = ttk.Entry(root, textvariable = self.date_start_variable)
        entry_date_start.place(x=150, y=70)
        label_date_end = ttk.Label(root, text = "Workshopende in der\nForm 2023-11-23")
        label_date_end.place(x=5, y=110)
        entry_date_end = ttk.Entry(root, textvariable = self.date_end_variable)
        entry_date_end.place(x=150, y=110)

        #Dropdown Language de - 
        self.label_language = ttk.Label(root, text = "Wähle Sprache aus")
        self.label_language.place(x=5, y= 150)
        options = ["de","eng"]
        self.drop_language = tk.OptionMenu(root, self.language_variable, *options)
        self.drop_language.place(x=150, y=150)
        
        #Button Import Signature
        self.label_signature = ttk.Label(root, text="Standardmäßige Signatur\n Default: 'unterschrift.png'")
        self.label_signature.place(x=5, y=190)
        self.button_signature = ttk.Button(root, text = "Importiere\nSignatur", command = self.import_signature)
        self.button_signature.place(x=180, y=400)
        
        #Label Imported Signature
        label_signature = ttk.Label(root, textvariable = self.signature_label_variable)
        label_signature.place(x=150, y=190)
        
        #Change Title Font Size
        title_size_descr = ttk.Label(root, text="Titel Fontgröße:\n")
        title_size_descr.place(x=5, y=230)
        entry_title_size = ttk.Entry(root, textvariable=self.title_size)
        entry_title_size.place(x=150, y=230, width=30)
        
        #Label Participant Path File Name
        label_import_participants_descr = ttk.Label(root, text="TeilnehmerInnenliste:")
        label_import_participants_descr.place(x=5, y= 270)
        label_import_participants = ttk.Label(root, textvariable = self.participant_list_label_variable)
        label_import_participants.place(x=150, y=270)
        
        #Label Description path
        #label_import_description_descr = ttk.Label(root, text="Workshopbeschreibung:")
        #label_import_description_descr.place(x=5, y= 310)
        #label_import_description = ttk.Label(root, textvariable = self.description_label_variable)
        #label_import_description.place(x=150, y=310)
        
        #Label Folder Path name
        label_folderpath_descr = ttk.Label(root, text="Ablageort:")
        label_folderpath_descr.place(x=5, y=350)
        label_folderpath = ttk.Label(root, textvariable = self.folderpath_label_variable)
        label_folderpath.place(x=150, y=350)
        
        #Button bar bottom
        #Button Import Participant List
        self.button_import_participants = ttk.Button(root, text = "Importiere\nTeilnehmer", command = self.import_participants)
        self.button_import_participants.place(x=5, y=400, height=40, width=85)
        
        #Button Import Workshop Description
        self.button_import_description = ttk.Button(root, text = "Lösche\nEingaben", command = self.clear_instance_variables)
        self.button_import_description.place(x=350, y=450, height=40, width=85)

        #Button Choose Folder Path
        self.button_folderpath = ttk.Button(root, text = "Wähle\nAblageort", command = self.choose_folder)
        self.button_folderpath.place(x=95, y=400, height=40, width=85)

        #Button to save settings
        button_save = ttk.Button(root, text="Speichere\nEinstellungen", command = self.save)
        button_save.place(x=5, y=450, height=40, width=85)
        
        #Button to load settings
        button_load = ttk.Button(root, text="Lade\nEinstellungen", command=self.load)
        button_load.place(x= 95, y=450, height=40, width=85)
        
        #Button Create Certificates
        button_create = ttk.Button(root, text = "Erstelle\nZertifikate", command = self.create_certificates)
        button_create.place(x=450, y=450, height=40, width=280)
        
        #Description Section on right side
        
        #Workshop Title
        label_workshop_title = ttk.Label(root, text = "Bitte den Workshoptitel für das Zertifikat eintragen")
        label_workshop_title.place(x=350, y=5)
        entry_workshop_title = ttk.Entry(root, textvariable = self.workshop_title_variable)
        entry_workshop_title.place(x=350, y=25, width=380)
        
        #Workshop Description Lines - Bullet Points for Workshop Content 1-10
        label_workshop_descr_0 = ttk.Label(root, text = "Bitte Workshopinhalt mit maximal 10 Stichpunkten")
        label_workshop_descr_0.place(x=350, y=55)
        entry_workshop_descr_0 = ttk.Entry(root, textvariable= self.workshop_descr_0_variable)
        entry_workshop_descr_0.place(x=350, y=75, width=380)
        entry_workshop_descr_1 = ttk.Entry(root, textvariable= self.workshop_descr_1_variable)
        entry_workshop_descr_1.place(x=350, y=95, width=380)
        entry_workshop_descr_2 = ttk.Entry(root, textvariable= self.workshop_descr_2_variable)
        entry_workshop_descr_2.place(x=350, y=115, width=380)
        entry_workshop_descr_3 = ttk.Entry(root, textvariable= self.workshop_descr_3_variable)
        entry_workshop_descr_3.place(x=350, y=135, width=380)
        entry_workshop_descr_4 = ttk.Entry(root, textvariable= self.workshop_descr_4_variable)
        entry_workshop_descr_4.place(x=350, y=155, width=380)
        entry_workshop_descr_5 = ttk.Entry(root, textvariable= self.workshop_descr_5_variable)
        entry_workshop_descr_5.place(x=350, y=175, width=380)
        entry_workshop_descr_6 = ttk.Entry(root, textvariable= self.workshop_descr_6_variable)
        entry_workshop_descr_6.place(x=350, y=195, width=380)
        entry_workshop_descr_7 = ttk.Entry(root, textvariable= self.workshop_descr_7_variable)
        entry_workshop_descr_7.place(x=350, y=215, width=380)
        entry_workshop_descr_8 = ttk.Entry(root, textvariable= self.workshop_descr_8_variable)
        entry_workshop_descr_8.place(x=350, y=235, width=380)
        entry_workshop_descr_9 = ttk.Entry(root, textvariable= self.workshop_descr_9_variable)
        entry_workshop_descr_9.place(x=350, y=255, width=380)
        
        label_notification = ttk.Label(root, textvariable = self.notification_variable, relief="sunken")
        label_notification.place(x=350, y= 300, height= 150, width=380)
        

        tk.mainloop()

    def import_participants(self):
        #Open Window to choose .csv file
        participant_path = filedialog.askopenfilename(parent= self.button_import_participants , filetypes= (("CSV FILE",".csv, .CSV"), ("All Files", "*.*")), initialdir=self.start_path)
        self.participant_list_variable.set(participant_path)
        #shorten variable to only show file name
        self.participant_list_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , participant_path))
    
    def import_signature(self):
        #Open Window to choose image file
        signature_path= filedialog.askopenfilename(parent= self.button_signature , filetypes= (("Image File",".jpg .JPG .jpeg .JPEG .png .PNG"), ("All Files", "*.*")), initialdir=self.start_path)
        self.signature_variable.set(signature_path)
        #shorten variable to only show file name
        self.signature_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , signature_path))

    def choose_folder(self):
        self.start_path = self.BASE_DIR
        #Open Window to choose folder to save certificates
        folder_path = filedialog.askdirectory(initialdir = self.start_path)
        self.folderpath_variable.set(folder_path)
        #shortenvvariable to only show file name
        self.folderpath_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , self.folderpath_variable.get()))

    #Dummy method to be overwritten
    def create_certificates(self):
        pass

    #Save Settings of Workshop
    def save(self):
        files = [("JSON", "*.json"), ("All Files", "*.*")]
        save_filename = filedialog.asksaveasfilename(initialfile = f"{self.workshopname_variable.get()}.json", 
                                            defaultextension = files, filetypes = files)
        if save_filename:
            #Save all Variables into one set
            self.description["workshop_title"] = self.workshop_title_variable.get()
            self.wrap_descriptions()
            content = {"file_name": self.workshopname_variable.get(),
                            "start": self.date_start_variable.get(),
                            "end": self.date_end_variable.get(),
                            "participants": self.participant_list_variable.get(),
                            "folder": self.folderpath_variable.get(),
                            "signature": self.signature_variable.get(),
                            "language": self.language_variable.get(),
                            "title_font": self.title_size.get(),
                            "semester": self.semester.get(),
                            "description": self.description}
            with open (save_filename, "w", encoding="utf-8") as f:
                json_file = json.dump(content, f)
    
    #Load Settings for Workshop
    def load(self):
        load_filename =  filedialog.askopenfilename(parent= self.button_import_participants, 
                                                    filetypes= (("JSON", "*.json"), ("All Files", "*.*")), initialdir=self.start_path)
        if load_filename:
            with open(load_filename, "r", encoding="utf-8") as file:
                settings = json.load(file)
                response_settings = input_checker.check_settings(settings)
                if len(response_settings) == 0:
                    self.notification_variable.set("Einstellungen wurden erfolgreich geladen.")
                else:
                    self.notification_variable.set(f"Die folgenden Keys fehlen in dem JSON-File\n{response_settings}")
                self.workshopname_variable.set(settings["file_name"])
                self.date_start_variable.set(settings["start"])
                self.date_end_variable.set(settings["end"])
                self.participant_list_variable.set(settings["participants"])
                self.participant_list_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , settings["participants"]))
                self.folderpath_variable.set(settings["folder"])
                self.folderpath_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , settings["folder"]))           
                self.signature_variable.set(settings["signature"])
                self.signature_label_variable.set(re.sub(r"(.*?)([\.\-\w]+)$", r"\2" , settings["signature"]))
                self.language_variable.set(settings["language"])
                self.title_size.set(settings["title_font"])
                self.semester.set(settings["semester"])
                self.workshop_title_variable.set(settings["description"]["workshop_title"])
                #Unpack List for single lines of workshop content
                for idx, stringvar in enumerate(self.descr_list):
                    stringvar.set(settings["description"]["workshop_content"][idx])
                
    #Takes all descriptions rows and glues them together
    def wrap_descriptions(self):
        #First delete List, to add new content
        self.description["workshop_content"].clear()
        for stringvar in self.descr_list:
            if stringvar.get():
                self.description["workshop_content"].append(stringvar.get())
            else:
                self.description["workshop_content"].append("")
                
    def clear_instance_variables(self):
        #Set Instance Variabls back to default
        self.signature_variable.set(os.path.join(self.BASE_DIR, "unterschrift.png"))
        self.title_size.set(70)
        
        #Collect all Instance Variables except for those with default values
        variable_list = [self.workshopname_variable, self.date_start_variable, self.date_end_variable, 
                        self.participant_list_variable, self.participant_list_label_variable,
                        self.folderpath_variable, self.folderpath_label_variable, self.signature_variable,
                        self.signature_label_variable, self.language_variable, self.title_size, self.semester,
                        self.workshop_title_variable]
        for element in self.descr_list:
            variable_list.append(element)
            
        #Set all instance variables back to empty string
        for element in variable_list:
            element.set("")
