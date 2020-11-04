# coding: utf-8
#filter_cases.py

import csv
import unicodedata

def main():
    with open('.//data//database.csv', 'r', encoding='utf-8') as file, open('.//filtered_data//newDataBase.csv', 'w', encoding='utf-8', newline='') as newFile:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(newFile, reader.fieldnames)
        writer.writeheader()

        for row in reader:
            if row['Resultado do Teste'].rstrip().lower() == 'positivo' and row['MunicÃ­pio de ResidÃªncia'].lower() == 'campina grande':
                writer.writerow(row)
        
main()
