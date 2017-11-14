#!/usr/bin/python3

import argparse

#Creates the new dsv file, with txt extension
def writeDsv(fileName, dsv):
    fileName = fileName[:-4]
    dsvFile = open(fileName + '.txt', 'w')
    dsvFile.write(dsv)    

#Parses the arguments
def parseArgs():
    parser = argparse.ArgumentParser(description='Csv file conversion.')
    parser.add_argument('-d', '--delimiter',
                        action='store',
                        default=' ',
                        help='Defines delimiter to use. SPACE is used as default.')
    parser.add_argument('-f',
                        action='append',
                        dest='files',
                        required=True,
                        help='Add file to conversion list')
    arguments = parser.parse_args()
    return arguments

#Converts the csv file to dsv file
def convert(fileName, delimiter):
    csv = open(fileName, 'r')
    dsv = ""
    for line in csv.readlines():
        columns = line.split(',')
        for column in columns[:-1]:
            dsv += column + delimiter
        dsv += columns[-1]
        dsv += '\n'
    return dsv

#Programm to convert from a csv file to a delimiter separated value (dsv) file save as a txt file
def main():
    try:
        arguments = parseArgs()
        for fileName in arguments.files:
            if (fileName[-4:] != '.csv'):
                raise NameError(fileName + "is not a csv file")
            dsv = convert(fileName, arguments.delimiter)
            writeDsv(fileName, dsv)
        
    except NameError as e:
        print(e)

if __name__  == "__main__":
    main()
