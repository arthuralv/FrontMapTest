# coding: utf-8
# Filter de casos da Paraíba por habitantes

import csv
import math

# Arredondamento, até 1 ou 2 casas
def format_number(num = 0, popCity = 1):
    num = (1000 * num) / popCity
    integ_n, float_n = str(num).split('.')
    float_n = str(math.ceil(float(float_n[:3]) / 10) * 10)

    return float(integ_n + '.' + str(float_n))

def find_city(city, cityFile):
    dictionary = csv.DictReader(cityFile)

    for row in dictionary:
        if row['city'] == city:
            return int(row['pop'])
    
    return 1

# João Pessoa: 16.566 / 20,48 por 1.000 habitantes
def show_cases(case_list):
    text = ''
    for elem in case_list:
        text += (capitalize(elem[2]) + ": " + thousand_format(elem[0]) + " / " + decimal_format(elem[1]) + " por 1.000 habitantes\n")
    
    return text
    
# Alagoinha: 39,83 por 1000 habitantes / 577
def show_cases_per_hab(case_list):
    text = ''
    for elem in case_list:
        text += (capitalize(elem[2]) + ": " + decimal_format(elem[0]) + " por 1.000 habitantes / " + thousand_format(elem[1]) + "\n")
    
    return text

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

    city_with_highest_cases = capitalize(list_cities_cases[-1][2])
    number_of_cases = thousand_format(list_cities_cases[-1][0])

    city_with_highest_cases_ph = capitalize(list_per_hab[-1][2])
    number_of_cases_ph = decimal_format(list_per_hab[-1][0])

    text = f'''
A foto acima é um mapa de calor (Heat Map) que mostra a quantidade de casos confirmados de COVID-19 por 1.000 habitantes, de acordo com cada região da Paraíba até o dia {day}/{mouth}/{year} às {hour}:{minute} hora(s), no total de {total} casos.

A intensidade das cores representam a escala de quantidade de casos por 1.000 habitantes em cada cidade.


Atualmente a área com maior número de casos na Paraíba é de {number_of_cases}, em {city_with_highest_cases}. Entretanto, a cidade com maior número de casos por 1.000 habitantes é {city_with_highest_cases_ph} com {number_of_cases_ph} aproximadamente. 
As 5 cidades com maior quantidade de casos:
{show_cases(list_cities_cases)}
As 5 cidades com maior quantidade de casos por 1000 habitantes:
{show_cases_per_hab(list_per_hab)}
'''
    return text
    
def read_write_data(fileReader, fileWriter):
    list_cities_cases = []
    list_per_hab = []
    total = 0

    for row in fileReader:
        if row['state'] == 'PB':
            if row['city'] != 'CASO SEM LOCALIZAÇÃO DEFINIDA/PB':
                city = row['city'][:-3].upper()
                cases = int(row['totalCases'])

                with open('.//data//popOrder.csv', 'r', encoding='utf8') as cityFile:
                    n_1000 = format_number(cases, find_city(city, cityFile))
                
                list_cities_cases.append((cases, n_1000, city))
                list_per_hab.append((n_1000, cases, city))

                fileWriter.writerow({'city': city, 'Ncasos': cases, 'Ncasos/1000H': n_1000})
                
                total += cases

    list_cities_cases.sort()
    list_per_hab.sort()

    return list_cities_cases[-5:], list_per_hab[-5:], total

def main():
    with open('.//data//cases_per_hab_pb.csv', 'r', encoding='utf8') as mainFile, open('.//filtered_data//cases_per_hab_pb_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, ['city', 'Ncasos', 'Ncasos/1000H'])

        fileWriter.writeheader()

        list_cities_cases, list_per_hab, total = read_write_data(fileReader, fileWriter)

    day = input("Digite o dia: ").zfill(2)
    mouth = input("Digite o mês: ").zfill(2)
    year = input("Digite o ano: ").zfill(2)

    hour = input("Digite a hora: ").zfill(2)
    minute = input("Digite o minuto: ").zfill(2)

    print(show_legend((list_cities_cases, list_per_hab), thousand_format(total), (day, mouth, year), (hour, minute)))

main()