# Made by Sangpil Kim
# 2016 June

import os
import csv
import argparse as arg

def concatCSV(sourceCSV,dstCSV):
    f = open(sourceCSV)
    # add line by line in to target CSV file
    for line in f:
         dstCSV.write(line)
    # close added file
    f.close()

def flattenCSV(sourceDir):
    # int for counting csv files
    counter = 0
    # Destination CSV file
    dstCSVname = sourceDir+'_concat.csv'
    #Get current path
    currentDir = os.getcwd()
    #Join currentPath and destination csv filename
    dstCSVpath = os.path.join(currentDir,dstCSVname)
    # if for check exist of destination csv file
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
    parser.add_argument('--foldername', default = '', type = str, help = 'Name of folder with multiple csv files')
    args = parser.parse_args()
    flattenCSV(args.foldername)


