import csv

# Read CSV file with csv.DicReader
def readCSV(fileName):
    with open(fileName,'rU') as csvfile:
        conts = []
        address = []
        ocupations = []
        reader = csv.DictReader(csvfile)
        n = 2
        for row in reader:
            tmp = row['contributor']
            groups = tmp.split(',')
            second = groups[n-1].split(' ')
            tmp2 = second[-1] + ''.join(groups[n:])
            tmp3 = ''.join(groups[0]) + ' '.join(second[:-1])
            address.append(tmp2)
            conts.append(tmp3)
            ocupations.append(row['ocupation'])
    return conts, address,ocupations

conts, address, ocupations = readCSV("donor_by_name_concat_CLASS.csv")

print(conts[0])
print(address[0])
print(ocupations[0])
