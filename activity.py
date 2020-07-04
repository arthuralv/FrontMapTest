import csv
import unicodedata
from difflib import SequenceMatcher

def ehSemelhante(str1, str2):
   return SequenceMatcher(a=str1, b=str2).ratio() > .9

def main():
    bairros = {}
    bairros_csv = {}

    with open('cases_cg.csv', 'r', encoding='utf8') as db, open('newDataBase.csv', 'r', encoding='utf8') as filenow:
        dbReader = csv.DictReader(db)
        fileReader = csv.DictReader(filenow)

        for row in dbReader:
            bairro = row['bairro'].lower()
            bairro = unicodedata.normalize('NFKD', bairro).encode('ASCII','ignore').decode('ASCII').rstrip()
            if bairro in bairros:
                bairros[bairro] += 1
            else:
                bairros[bairro] = 0
        
        for row in fileReader:
            bairro = row['Bairro'].lower()
            bairro = unicodedata.normalize('NFKD', bairro).encode('ASCII','ignore').decode('ASCII').rstrip()
            if bairro in bairros_csv:
                bairros_csv[bairro] += 1
            else:
                bairros_csv[bairro] = 0
        
        for bairro in bairros:
            for bairro_csv in bairros_csv:
                if ehSemelhante(bairro, bairro_csv):
                    bairros[bairro] += bairros_csv[bairro_csv]
        
    with open('cases_cg.csv', 'r', encoding='utf8') as reference, open('cases_cg_filtered.csv', 'w', newline='\n', encoding='utf8') as db:
        dbWriter = csv.DictWriter(db, dbReader.fieldnames)
        dbWriter.writeheader()
        refReader = csv.DictReader(reference)

        for row in refReader:
            dbWriter.writerow({'bairro': row['bairro'], 'cases': bairros[unicodedata.normalize('NFKD', row['bairro'].lower()).encode('ASCII','ignore').decode('ASCII').rstrip()]})


main()
