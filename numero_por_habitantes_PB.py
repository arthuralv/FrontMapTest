# coding: utf-8
# Filter de casos da paraíba por habitantes

import csv
import math

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

def show_cases(case_list):
    for elem in case_list:
            print(capitalize(elem[2]) + ':', thousand_format(elem[0]), '/', decimal_format(elem[1]), 'por 1000 habitantes')
    else:
        text1 = 'por 1.000 habitantes'
    # Exemplo = Patos: 1,306 / 12.14 por 1,000 habitantes

def show_cases_per_hab(case_list):
    for elem in case_list:
            print(capitalize(elem[2]) + ':', decimal_format(elem[0]), 'por 1000 habitantes', '/', thousand_format(elem[1]))
    
def thousand_format(num):
    return f'{num:,}'.replace(',','.')

def decimal_format(num):
    return f'{num}'.replace('.',',')

def capitalize(phrase):
    phrase_list = phrase.split()
    new = phrase_list[0].capitalize()

    for i in range(1, len(phrase_list)):
        new += ' ' + phrase_list[i].capitalize() if len(phrase_list[i]) > 2 else ' ' + phrase_list[i].lower()

    return new

def showLegend(lista, hab, total):
    
    days = '13'
    mouths = '07'
    years = '20'

    hours = '11'
    minutes = '00'

    cidade_MQdC = capitalize(lista[-1][2])
    casos_MQdC = thousand_format(lista[-1][0])

    cidade_MQdC_PH = capitalize(hab[-1][2])
    casos_MQdC_PH = decimal_format(hab[-1][0])

    print(
f'''A foto acima é um mapa de calor (Heat Map) que mostra a quantidade de casos confirmados de COVID-19 por 1000 habitantes, de acordo com cada região da Paraíba até o dia {days}/{mouths}/{years} às {hours}:{minutes} hora(s), no total de {total} casos.

A intensidade das cores representam a escala de quantidade de casos por 1000 habitantes em cada cidade.

Atualmente a área com maior número de casos na Paraíba é de {casos_MQdC}, em {cidade_MQdC}. Entretanto, a cidade com maior número de casos por 1000 habitantes é {cidade_MQdC_PH} com {casos_MQdC_PH} aproximadamente.
'''
        )
    
    print('As 5 cidades com maior quantidade de casos:')
    show_cases(lista)
    
    print('\n')

    print('As 5 cidades com maior quantidade de casos por 1000 habitantes:')
    show_cases_per_hab(hab)

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
    
    showLegend(lista[-5:], hab[-5:], thousand_format(soma))
    
main()