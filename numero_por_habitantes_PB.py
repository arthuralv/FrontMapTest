# coding: utf-8
# Filter de casos da paraíba por habitantes

import csv
import math

def main():
    lista = []
    hab = []
    soma = 0

    with open('cases_per_1000.csv', 'r', encoding='utf8') as mainFile, open('cases_per_1000_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)

        fileWriter = csv.DictWriter(writeFile, ['city', 'Ncasos', 'Ncasos/1000H'])
        fileWriter.writeheader()
        # Arredondamento, até 1 casa
        
        for row in fileReader:
            if row['state'] == 'PB':
                if row['city'] != 'CASO SEM LOCALIZAÇÃO DEFINIDA/PB':
                    city = row['city'][:-3].upper()
                    cases = int(row['totalCases'])
                    
                    n_1000 = float(formatar(int(cases), find(city)))
                    soma += int(cases)
                    
                    lista.append((cases, n_1000, city))
                    hab.append((n_1000, cases, city))
                    
                    fileWriter.writerow({'city': city, 'Ncasos': cases, 'Ncasos/1000H': n_1000})
        lista.sort()
        hab.sort()

    print('\nMAIORES NÚMEROS DE CASOS------')
    show(lista[-5:])
    print('\nMAIORES NÚMEROS POR 1000 HAB--')
    show(hab[-5:], 'hab')
    print('\n\nTOTAL DE CASOS:', soma)

def formatar(num = 0, popCity = 1):
    num = (1000 * num) / popCity
    inteiro, flutuante = str(num).split('.')
    flutuante = str(math.ceil(float(flutuante[:3]) / 10) * 10)
    return float(inteiro + '.' + str(flutuante))

def find(city):
    with open('popOrder.csv', 'r', encoding='utf8') as cityFile:
        dictionary = csv.DictReader(cityFile)

        for row in dictionary:
            if row['city'] == city:
                return int(row['pop'])
        return 1

def show(list, type='std'):
    text1 = ''
    text2 = ''

    if type == 'std':
        text2 = 'por 1,000 habitantes'
    else:
        text1 = 'por 1,000 habitantes'
    # Exemplo = Patos: 1,306 / 12.14 por 1,000 habitantes
    
    
    for elem in list:
        print(str(elem[2]).capitalize() + ':', text1, decimalFormat(elem[0]), '/', decimalFormat(elem[1]), text2)
    
def decimalFormat(num):
    return '{:,}'.format(num)

main()