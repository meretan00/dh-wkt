import re

#Module to check the input of the certificator GUI
def check_semester(semester):
    #Semester Jahreszahl oder Semester Jahreszahl/Jahreszahl
    matches = re.search(r"\w+\s\d+(\/\d+)?$", semester)
    if matches:
        return ""
    else:
        return f"'{semester}' entspricht nicht dem Muster des Feldes 'Semester'\nz.B. Wintersemester 24/25 oder Sommersemester 25\n"
    
def check_prefix(prefix):
    matches = re.match(r"\d{6,8}_\w+", prefix)
    if matches:
        return ""
    else:
        return f"'{prefix}' entspricht nicht dem Muster des Feldes 'Filepräfix'\nz.B. 241124_XML\n"
    
def check_time(time):
    matches = re.match(r"\d{4}-\d{2}-\d{2}$", time)
    if matches:
        return ""
    else:
        return f"'{time}' entspricht nicht dem Muster des Zeitfeldes\nz.B. 2024-11-24\n"
    
#returns a list of missing keys in json for proper settings
def check_settings(json_file):
    missing_keys =[]
    necessary_keys = ("file_name", "start", "end", "participants", "folder", "signature", "language", "title_font", "semester", "description")
    for key in necessary_keys:
        if key not in json_file:
            missing_keys.append(key)
    return missing_keys

#settings = {"file_name": None, "start":None, "end":None, "participants":None,
 #           "folder": None, "signature": None, "language": None, "title_font": None, "semester": None}

