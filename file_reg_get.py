import logging
import csv

REG_FILE = 'DataFiles/20200531-WorkerAssignment.csv'

#Set Logging Level to print out
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    #,filename = 'basic.log'
)

def read_ax_reg(filename = REG_FILE):
    '''Read the WorkerAssignment csv file. Build a list of dictionaries from this information.
    Not needed if reading data from the get_registrations API call'''

    logging.info('Entering read_ax_reg')
    logging.debug(f'Setting up empty reg_list inside read_ax_reg.')

    reg_list = []
    with open(filename, newline = '') as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '"')
        for row in file_reader:
            reg_list.append(row)

    logging.info('Leaving read_ax_reg')
    logging.debug(f'Returning reg_list from read_reg_file.read_ax_reg: {reg_list}')

    return 'FILE', reg_list
