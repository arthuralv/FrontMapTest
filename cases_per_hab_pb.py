# coding: utf-8
# Filter de casos da Paraíba por habitantes

import csv
import math

# Arredondamento, até 1 ou 2 casas
def format_number(num = 0, popCity = 1):
    num = (1000 * num) / popCity
    inteiro, flutuante = str(num).split('.')
    flutuante = str(math.ceil(float(flutuante[:3]) / 10) * 10)

    return float(inteiro + '.' + str(flutuante))

def find_city(city):
    with open('.//data//popOrder.csv', 'r', encoding='utf8') as cityFile:
        dictionary = csv.DictReader(cityFile)

        for row in dictionary:
            if row['city'] == city:
                return int(row['pop'])
        
        return 1

# João Pessoa: 16.566 / 20,48 por 1.000 habitantes
def show_cases(case_list):
    for elem in case_list:
        print(capitalize(elem[2]) + ':', thousand_format(elem[0]), '/', decimal_format(elem[1]), 'por 1.000 habitantes')
    
# Alagoinha: 39,83 por 1000 habitantes / 577
def show_cases_per_hab(case_list):
    for elem in case_list:
        print(capitalize(elem[2]) + ':', decimal_format(elem[0]), 'por 1.000 habitantes', '/', thousand_format(elem[1]))

# 1000 = 1.000    
def thousand_format(num):
    return f'{num:,}'.replace(',','.')

# 0.1231 = 0,1231
def decimal_format(num):
    return f'{num}'.replace('.',',')

# São josé da mata = São José da Mata
def capitalize(phrase):
    phrase_list = phrase.split()
    new = phrase_list[0].capitalize()

    for i in range(1, len(phrase_list)):
        new += ' ' + phrase_list[i].capitalize() if len(phrase_list[i]) > 2 else ' ' + phrase_list[i].lower()

    return new

def show_legend(lists, total, date, time):
    list_cities_cases, list_per_hab = lists
    day, mouth, year = date
    hour, minute = time

    cidade_MQdC = capitalize(list_cities_cases[-1][2])
    casos_MQdC = thousand_format(list_cities_cases[-1][0])

    cidade_MQdC_PH = capitalize(list_per_hab[-1][2])
    casos_MQdC_PH = decimal_format(list_per_hab[-1][0])

    print(
f'''A foto acima é um mapa de calor (Heat Map) que mostra a quantidade de casos confirmados de COVID-19 por 1.000 habitantes, de acordo com cada região da Paraíba até o dia {days}/{mouths}/{years} às {hours}:{minutes} hora(s), no total de {total} casos.

A intensidade das cores representam a escala de quantidade de casos por 1.000 habitantes em cada cidade.

Atualmente a área com maior número de casos na Paraíba é de {casos_MQdC}, em {cidade_MQdC}. Entretanto, a cidade com maior número de casos por 1.000 habitantes é {cidade_MQdC_PH} com {casos_MQdC_PH} aproximadamente.
'''
        )
    
    print('As 5 cidades com maior quantidade de casos:')
    show_cases(list_cities_cases)
    
    print('\n')

    print('As 5 cidades com maior quantidade de casos por 1000 habitantes:')
    show_cases_per_hab(list_per_hab)

def read_write_data(fileReader, fileWriter):
    list_cities_cases = []
    list_per_hab = []
    total = 0

    for row in fileReader:
        if row['state'] == 'PB':
            if row['city'] != 'CASO SEM LOCALIZAÇÃO DEFINIDA/PB':
                city = row['city'][:-3].upper()
                cases = int(row['totalCases'])
                n_1000 = format_number(cases, find_city(city))
                
                list_cities_cases.append((cases, n_1000, city))
                list_per_hab.append((n_1000, cases, city))
                
                fileWriter.writerow({'city': city, 'Ncasos': cases, 'Ncasos/1000H': n_1000})
                
                total += cases

    list_cities_cases.sort()
    list_per_hab.sort()

    return list_cities_cases[-5:], list_per_hab[-5:], total

def main():
    with open('.//data//cases_per_1000.csv', 'r', encoding='utf8') as mainFile, open('.//filtered_data//cases_per_1000_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, ['city', 'Ncasos', 'Ncasos/1000H'])

        fileWriter.writeheader()

        list_cities_cases, list_per_hab, total = read_write_data(fileReader, fileWriter)

    day = input("Digite o dia: ").zfill(2)
    mouth = input("Digite o mês: ").zfill(2)
    year = input("Digite o ano: ").zfill(2)

    hour = input("Digite a hora: ").zfill(2)
    minute = input("Digite o minuto: ").zfill(2)

    show_legend((list_cities_cases, list_per_hab), thousand_format(total), (day, mouth, year), (hour, minute))

main()