import csv
import logging

#Set Logging Level to print out
logging.basicConfig(
    level = logging.DEBUG, #Levels are DEBUG, INFO, WARNING, ERROR and CRITICAL
    format = '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    #,filename = 'basic.log'
)


def read_locked_work_file(filename = 'DataFiles/Locked_work_assignments.txt'):
    '''Read the Locked_work_assignment csv file to build a list of locked work assignments (like course_setup and safety)'''

    logging.info('Entering read_locked_work_file')
    logging.debug(f'Setting up empty work_list inside read_locked_work_file.')

    work_list = []
    with open(filename, newline = '') as csvfile:
        file_reader = csv.DictReader(csvfile, delimiter = ',')
        for row in file_reader:
            logging.debug(f'row being sent through in for loop: {row}')
            work_list.append((row['Name'], row['Work_Position']))

    logging.info('Leaving read_locked_work_file')
    logging.debug(f'Returning work_list: {work_list}')

    return work_list

print(read_locked_work_file())