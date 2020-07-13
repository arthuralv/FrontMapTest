# coding: utf-8
# Filter de casos da Paraíba por data

import csv

def main():
    # {'data':, 'totalDeCasos':}
    date_map = {}

    with open('cases_per_date.csv', 'r', encoding='utf8') as mainFile, open('cases_per_date_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)

        fileWriter = csv.DictWriter(writeFile, ['data', 'qtdCasos'])
        fileWriter.writeheader()
        count = 30
        for row in fileReader:
            if row['state'] == 'PB':
                date = row['date']
                cases = int(row['totalCases'])
                
                if date in date_map:
                    date_map[date] += cases
                else:
                    date_map[date] = cases
                
        for date in date_map:
            fileWriter.writerow({'data': date, 'qtdCasos': date_map[date]})
            
main()