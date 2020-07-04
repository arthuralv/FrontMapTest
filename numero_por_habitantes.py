# coding: utf-8
# Filter de casos da paraíba por habitantes

import csv
import math

def main():
    lista = []
    hab = []
    soma = 0

    with open('cases_1000_habitantes.csv', 'r', encoding='utf8') as mainFile, open('cases_per_1000_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, fileReader.fieldnames)
        fileWriter.writeheader()
        # Arredondamento, até 1 casa
        
        for row in fileReader:

            if row['Ncasos/1000H'] != None:
                lista.append((int(row['Ncasos']), row['city'].capitalize()))
                n_1000 = formatar(row['Ncasos/1000H'])
                hab.append((float(n_1000), row['city'].capitalize()))
                
                fileWriter.writerow({'city': row['city'], 'Ncasos': row['Ncasos'], 'Ncasos/1000H': n_1000})

            soma += int(row['Ncasos'])

        lista.sort()
        hab.sort()

    new = lista[-5:]
    for elem in new:
        print(str(elem[1]) + ':', elem[0])

    print('------------------------------')

    new = hab[-5:]
    for elem in new:
        print(str(elem[1]) + ':', elem[0])
    print(soma)

def formatar(num = 0):
    inteiro, flutuante = str(num).split('.')
    flutuante = str(math.ceil(float(flutuante[:3]) / 10) * 10)
    return float(inteiro + '.' + str(flutuante))

main()