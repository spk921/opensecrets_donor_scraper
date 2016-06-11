# Made by Sangpil Kim
# 2016 June

import os
import csv

def concatCSV(sourceCSV,dstCSV):
    f = open(sourceCSV)
    # add line by line in to target CSV file
    for line in f:
         dstCSV.write(line)
    # close added file
    f.close()

def flattenCSV(sourceDir):
    # set path of folder which has CSV files
    sourceDir = 'donor_by_name'
    counter = 0
    # Destination CSV file
    dstCSVname = sourceDir+'_concat.csv'
    currentDir = os.getcwd()
    dstCSVpath = os.path.join(currentDir,dstCSVname)
    if not os.path.isfile(dstCSVpath):
        dstCSV=open(dstCSVname,"a")
        targetDir = os.path.join(os.getcwd(),sourceDir)
        # iter files
        for csvFile in os.listdir(targetDir):
            sourceCSV = os.path.join(targetDir,csvFile)
            if csvFile.endswith('.csv'):
                if os.path.isfile(sourceCSV):
                    concatCSV(sourceCSV,dstCSV)
                    counter += 1
                    continue
                else:
                    continue
        print('%d csv found and concated' %(counter))
        # Close target CSV file
        dstCSV.close()
    else:
        print('Destination CSV file exist')

if __name__ == "__main__":
    parser = arg.ArgumentParser()
    parser.add_argument('--dest', default = '', type = str, help = 'Name of folder with multiple csv files')
    args = parser.parse_args()
    flattenCSV(args.dest)

