# coding: utf-8

from csv import DictReader, DictWriter
from difflib import SequenceMatcher
from unicodedata import normalize
from datetime import datetime
import pandas as pd

def is_similar(str1, dict1):
    for value in dict1.values():
        if SequenceMatcher(a=str1, b=value).ratio() > .9: return True
    return False

def main():
    bairros = {}

    with open('.//data//cases_cg.csv', 'r', encoding='utf8') as read_file:
        reader = DictReader(read_file)

        for row in reader:
            bairro = normalize('NFKD', row['bairro']).encode('ASCII','ignore').decode('ASCII').upper().rstrip()
            if not (bairro in bairros):
                bairros[bairro] = []
    
    with open('.//data//CgBairrosFiltrados.csv', 'r', encoding='utf8') as read_file:
        reader = DictReader(read_file)
        error = [] # lista dos bairros que deram errado / não existem

        for row in reader:
            r_bairro = normalize('NFKD', row['Bairro']).encode('ASCII','ignore').decode('ASCII').upper().rstrip()
            try:
                dia, mes, ano = row['Data'].split('/')
                data = dia.zfill(2) + '-' + mes.zfill(2) + '-' + ano.zfill(2)

                if r_bairro in bairros:
                    bairros[r_bairro].append((r_bairro, data))
                elif is_similar(r_bairro, bairros):
                    bairros[r_bairro].append((r_bairro, data))
                else:
                    error.append(row)
            except ValueError:
                error.append(row)
                continue
    
    for bairro in bairros:
        lista = sorted(bairros[bairro], key=lambda x: datetime.strptime(x[1], '%d-%m-%Y'))
        arquivo =  bairro.lower().replace(' ', '_')
        inicio = lista[0][1]
        fim = lista[-1][1]

        with open('.//data//bairros//' + arquivo + '.csv', 'w', encoding='utf8', newline='\n') as write_file:
            writer = DictWriter(write_file, ['bairro', 'data'])
            writer.writeheader()

            for elem in lista:
                writer.writerow({'bairro': elem[0], 'data': elem[1]})

        with open('.//data//bairros//' + arquivo + '.csv', 'r', encoding='utf8') as read_file, open('.//data//bairros_filtrados//' + arquivo + '_filtrado.csv', 'w', encoding='utf8', newline='\n') as write_file:
            reader = DictReader(read_file)
            writer = DictWriter(write_file, ['bairro', 'data', 'casos'])
            writer.writeheader()
            date_map = dict(map(lambda a: (str(a)[:10], 1), pd.date_range(start=inicio, end=fim, normalize=True)))
            total = 1

            for row in reader:
                date = row['data']
                
                if date in date_map:
                    total += 1
                    date_map[date] = total
                else:
                    date_map[date] = total

            for date in date_map:
                writer.writerow({'bairro': bairro, 'data': date, 'casos': date_map[date]})



main()