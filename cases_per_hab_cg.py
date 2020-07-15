import csv
from unicodedata import normalize
from math import ceil
from difflib import SequenceMatcher

def is_similar(str1, str2):
   return SequenceMatcher(a=str1, b=str2).ratio() > .9

def formatar(num = 0):
    inteiro, flutuante = str(num).split('.')
    flutuante = str(ceil(float(flutuante[:3]) / 10) * 10)
    return float(inteiro + '.' + str(flutuante))

def main():
    bairros = {}
    bairros_csv = {}

    with open('.//data//cases_per_hab_cg.csv', 'r', encoding='utf8') as db, open('.//data//cases_per_hab_cg_filtered.csv', 'r', encoding='utf8') as filenow:
        dbReader = csv.DictReader(db)
        fileReader = csv.DictReader(filenow)

        for row in dbReader:
            bairro = row['bairro'].lower()
            bairro = normalize('NFKD', bairro).encode('ASCII','ignore').decode('ASCII').rstrip()
            if bairro in bairros:
                bairros[bairro] += 1
            else:
                bairros[bairro] = 0
        
        for row in fileReader:
            bairro = row['Bairro'].lower()
            bairro = normalize('NFKD', bairro).encode('ASCII','ignore').decode('ASCII').rstrip()
            if bairro in bairros_csv:
                bairros_csv[bairro] += 1
            else:
                bairros_csv[bairro] = 0
        
        for bairro in bairros:
            for bairro_csv in bairros_csv:
                if is_similar(bairro, bairro_csv):
                    bairros[bairro] += bairros_csv[bairro_csv]
        
    with open('.//data//cases_cg.csv', 'r', encoding='utf8') as reference, open('.//filtered_data//cases_cg_filtered.csv', 'w', newline='\n', encoding='utf8') as db:
        dbWriter = csv.DictWriter(db, dbReader.fieldnames + ['n/1000'])
        dbWriter.writeheader()
        refReader = csv.DictReader(reference)

        for row in refReader:
            casos = bairros[normalize('NFKD', row['bairro'].lower()).encode('ASCII','ignore').decode('ASCII').rstrip()]

            dbWriter.writerow({'bairro': row['bairro'], 'cases': casos, 'n/1000': formatar(casos/1000)})

main()