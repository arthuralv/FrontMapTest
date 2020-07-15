# coding: utf-8
# Filter de casos da Paraíba por data

import csv

def filter_data(date_map, fileReader):
    for row in fileReader:
        if row['state'] == 'PB':
            date = row['date']
            cases = int(row['totalCases'])
            
            if date in date_map:
                date_map[date] += cases
            else:
                date_map[date] = cases

def write_data(date_map, fileWriter):
    for date in date_map:
            fileWriter.writerow({'data': date, 'qtdCasos': date_map[date]})

def main():
    # {'data':, 'totalDeCasos':}
    date_map = {}

    with open('.//data//cases_per_date_pb.csv', 'r', encoding='utf8') as mainFile, open('.//filtered_data//cases_per_date_pb_filtered.csv', 'w', newline='\n', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, ['data', 'qtdCasos'])

        fileWriter.writeheader()
        filter_data(date_map, fileReader)
        write_data(date_map, fileWriter)
                
main()