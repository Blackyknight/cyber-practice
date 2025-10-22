# Simple Python script to organize files in a given folder into subfolders by extension.

import os
import shutil

path = input("Enter the folder path: ")
print(f"You entered: {path}")

if not os.path.exists(path):
    print("The specified path does not exist.")

else:
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        print(f"Processing file: {filePath}")

        if os.path.isfile(filePath):
            ext = file.split('.')[-1]
            print(f"File extension: {ext}")
            targetFolder = os.path.join(path, ext.upper() + "_files")
            print(f"Target folder: {targetFolder}")
            os.makedirs(targetFolder, exist_ok=True)
            shutil.move(filePath, os.path.join(targetFolder, file))

print(f"File organization complete in {path}")