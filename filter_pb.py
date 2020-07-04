# Filter do estado da Paraíba
# coding: utf-8

import csv

def main():
    lista = []
    with open('cases_cities.csv', 'r', encoding='utf8') as mainFile, open('cases_cg_filtered.csv', 'w', newline='', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, fieldnames=['city', 'cases'])
        fileWriter.writeheader()
        soma = 0

        for row in fileReader:
            if row['state'] == 'PB':
                fileWriter.writerow({'city': row['city'].upper()[:-3], 'cases': row['totalCases']})
                lista.append((int(row['totalCases']), row['city'][:-3]))
                
                soma += int(row['totalCases'])
        lista.sort()

    new = lista[-5:]
    for elem in new:
        print(str(elem[1]) + ':', elem[0])

    string = f"A foto acima é um mapa de calor (Heat Map) que mostra os casos confirmados de COVID-19 de acordo com cada região da Paraíba até o dia 22/06/20 às 16 horas, no total de {soma} casos. A intensidade das cores representam a escala de quantidade de casos por cidade. Atualmente a área com maior número de casos na Paraíba é de {new[4][1]}, em {new[4][0]}.\nAs 5 cidades com maior quantidade de casos:\n{new[0][1]}: {new[0][0]}\n{new[1][1]}: {new[1][0]}\n{new[2][1]}: {new[2][0]}\n{new[3][1]}: {new[3][0]}\n{new[4][1]}: {new[4][0]}\n\nOs dados podem ser acessados através do link na bio.\n\nBoa tarde a todos.\n\n#covid19 #machinelearning #artificialinteligence #UFCG #UEPB #NUTES #IFPB"

    print(string)

main()