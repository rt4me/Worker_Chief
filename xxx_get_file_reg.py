import logging
import csv

# REG_FILE = 'DataFiles/20200531-WorkerAssignment.csv'


#No longer used; placed this functionality in build_participant_dict.py file

# def read_ax_reg(filename = REG_FILE):
#     '''Read the WorkerAssignment csv file. Build a list of dictionaries from this information.
#     Not needed if reading data from the get_reg_assignments API call'''
#
#     logging.info('Entering read_ax_reg')
#     logging.debug(f'Setting up empty reg_list inside read_ax_reg.')
#
#     reg_list = []
#     with open(filename, newline = '') as csvfile:
#         file_reader = csv.DictReader(csvfile, delimiter = ',', quotechar = '"')
#         for row in file_reader:
#             reg_list.append(row)
#
#     logging.info('Leaving read_ax_reg')
#     logging.debug(f'Returning reg_list from read_reg_file.read_ax_reg: {reg_list}')
#
#     return 'FILE', reg_list
