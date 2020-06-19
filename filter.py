import csv

def main():
    lista = []
    with open('cases_cities.csv', 'r', encoding='utf8') as mainFile, open('cases_cities_filtered.csv', 'w', newline='', encoding='utf8') as writeFile:
        fileReader = csv.DictReader(mainFile)
        fileWriter = csv.DictWriter(writeFile, fieldnames=['city', 'cases'])
        fileWriter.writeheader()

        for row in fileReader:
            if row['state'] == 'PB':
                fileWriter.writerow({'city': row['city'].upper()[:-3], 'cases': row['totalCases']})
                lista.append((int(row['totalCases']), row['city'][:-3]))
                lista.sort()
    new = lista[-5:]
    for elem in new:
        print(str(elem[1]) + ': ', elem[0])
main()