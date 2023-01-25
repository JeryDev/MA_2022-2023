#In diesem Programm wird veranschaulicht, wie die einzelnen Dateien erstellt, auf Existenz geprüft und gesucht werden.

import os
import json
import openpyxl as xl
import platform

#Systemabfrage und Pfad zum Desktop
if platform.system() == "Darwin":
  #MacOS
  folder_path = os.path.join(os.environ["HOME"], "Desktop", "Matura_Jery")
  file_path_xlsx = os.path.join(os.environ["HOME"], "Desktop", "Matura_Jery", "data.xlsx")
  file_path_config = os.path.join(os.environ["HOME"], "Desktop", "Matura_Jery", "config.json")
elif platform.system() == "Windows":
  #Windows
  folder_path = os.path.join(os.environ["HOMEPATH"], "Desktop", "Matura_Jery")
  file_path_xlsx = os.path.join(os.environ["HOMEPATH"], "Desktop", "Matura_Jery", "data.xlsx")
  file_path_config = os.path.join(os.environ["HOMEPATH"], "Desktop", "Matura_Jery", "config.json")
else:
  #Rest
  exit("Unsupported System")

#Werte in Excel setzen
def setValue(row, column, tabel, value):
    tabel.cell(row=row, column=column).value = value

try:
  #Ordner wird gesucht
  if os.path.isdir(folder_path):
    print("Folder does exist!")
  else:
    #Ordner wird erstellt
    os.mkdir(folder_path)
    print("Folder has been created!")
  
  #Excel-Datei wird gesucht
  if os.path.isfile(file_path_xlsx): 
    print("Workbook does exist!")

  else:
    #Excel-Datei wird erstellt
    workbook = xl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Stats"
    setValue(1, 1, worksheet, "Test")
    workbook.save(file_path_xlsx)
    print("Workbook has been created!")

  #Konfigurationsdatei wird gesucht
  if os.path.isfile(file_path_config): 
    print("Configfile does exist!")

  else:
    #Konfigurationsdatei Standardwert wird gesetzt
    data = {
      "size": 1050
    }
    #Konfigurationsdatei wird erstellt
    with open(file_path_config, "w") as file:
      json.dump(data, file, indent=1)
      print("File has been created!")
                                      
  print(folder_path)
  print(file_path_xlsx)
  print(file_path_config)

except(KeyError, TypeError):
  print("Unsupported System: " + platform.system())
