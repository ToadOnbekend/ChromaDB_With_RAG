import os

FOLDERPdf ="tempTestUpload"

for filename in os.listdir(FOLDERPdf):
    file_path = os.path.join(FOLDERPdf, filename)
    os.remove(file_path)
    print(f"Bestand verwijderd: {file_path}")