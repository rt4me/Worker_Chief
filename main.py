import build_participant_dict
import logging
import csv

#Set Logging Level to print out
logging.basicConfig(
    level = logging.INFO, #Levels are DEBUG, INFO, WARNING, ERROR and CRITICAL
    format = '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    #,filename = 'basic.log'
)


AX_CLASS_LIST = 'DataFiles/AXClassList.txt'
AX_CLASS_MODIFIER_LIST = 'DataFiles/AXClassModifiers.txt'
MEDICAL_FILE = 'DataFiles/Medical.txt'
COURSE_SETUP_WORKERS = 'DataFiles/Locked_work_assignments.txt'


###################################################################################################################
#
#Building Participants list (via either API GET or using a manually retrieved report file from MSR)
#
###################################################################################################################

test_event_number = 4
test_event_year = 2022

def build_participant_list():

    source_resp = input("What source do you want to use for processing (API or FILE): ")

    if source_resp.upper() == 'API':
        year = input("What event year did you want to use (2020 to present): ") or test_event_year
        event_num = input("What event number did you want to use (1-9): ") or test_event_number

        logging.info('Getting Event ID')
        event_id = build_participant_dict.get_event_uri(event_num, year)

        logging.info('Getting registration list via API')
        api_full_reg_response = build_participant_dict.get_reg_assignments(event_id)

        logging.info('Building participant_list based on response getting full registration list')
        participant_list = build_participant_dict.data_source_from_api(api_full_reg_response[1])

        return participant_list

    if source_resp.upper() == 'FILE':

        logging.debug('Asking for user to enter file name and path for Worker Sheet Report')
        report_file_used = input('Enter path/name of Worker Assignment sheet (defaults to hard coded value): ') or 'DataFiles/20200531-WorkerAssignment.csv'
        logging.info(f'file entry value: {report_file_used}')

        logging.info('Getting registration list via report file (only taking the reg info, which is in the 2nd element from the main registration body')
        file_full_reg_response = build_participant_dict.read_ax_reg_file(report_file_used)[1]

        logging.info('Building participant_list based on response getting full registration list')
        participant_list = build_participant_dict.data_source_from_file(file_full_reg_response)

        return participant_list

    else:
        logging.info('Registration source not recognized as FILE or API')
        print('Registration source not recognized as FILE or API')


participant_list = build_participant_list()
#print(f'Print participan list: {participant_list}')

#Sort participant_list by Last Name
# participant_list_sorted = sorted(participant_list, key=lambda x: x.__dict__['lname'])
# print(f'Print participan list sorted by last name:{participant_list_sorted}')

#List of Novices:
# for x in participant_list:
#     #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
#     if x.__dict__['car_class'][0] == 'N':
#         print(x)





# def novice_list_and_count(participant_list = participant_list):
#     novice_cnt = 0
#     novice_list = []
#     for x in participant_list:
#         #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
#         if x.__dict__['car_class'][0] == 'N':
#             novice_cnt += 1
#             novice_list.append(x)
#     return(novice_cnt, novice_list)

# print(f'''Count of Novices: {novice_list_and_count()[0]}, Novice List: {novice_list_and_count()[1]}''')






###################################################################################################################
#
#Build Complete AX Class List
#
###################################################################################################################

def build_master_class_list(class_filename = AX_CLASS_LIST, class_mod_filename = AX_CLASS_MODIFIER_LIST):
    '''Building a master list of classes using the AXClassList.txt and AXClassModifiers.txt flat files.
    The master list will contain an entry for all "core" classes as well as an instance of each core class with a prefix (ex. N, X, M) or suffix (L) modifier.'''
    logging.info('Entering build_master_class_list')
    master_class_list = []
    class_list_temp = []
    with open(class_filename, 'r') as f:
        class_lines_list = f.readlines()
        for line in class_lines_list:
            class_list_temp.append(line.strip())
            master_class_list.append(line.strip())

    with open(class_mod_filename, newline = '') as m:
        class_mod_line_list = csv.DictReader(m, delimiter = ',')
        for mod_line in class_mod_line_list:
            logging.debug(f'Line from Class Mod List = {mod_line}')

            if mod_line['Position'].strip() == 'Prefix':
                logging.info(f'Processing Prefix Modifier Type; {mod_line}')
                for x in class_list_temp:
                    master_class_list.append(f'''{mod_line['Value'].strip()}{x.strip()}''')

            elif mod_line['Position'].strip() == 'Suffix':
                logging.info(f'Processing Suffix Modifier Type; {mod_line}')
                for x in class_list_temp:
                    master_class_list.append(f'''{x.strip()}{mod_line['Value'].strip()}''')

            else:
                logging.warning(f'Unknown class modifier type attempting to be used: {mod_line} ')
    logging.debug(f'Returning master_class_list with all classes: {master_class_list}')
    logging.info('Leaving build_master_class_list')
    return master_class_list

print(f'List of all classes: {build_master_class_list()}')



#print(f'List of people requesting to work Set Up: {find_requested_course_setup(read_ax_reg())}')
#print(f'List of unapproved setup workers: {find_invalid_setup_workers(read_ax_reg(), read_course_setup())}')
#print(f'List of unapproved setup workers: {find_invalid_setup_workers(reg_list, read_course_setup())}')

if __name__ == '__main__':
    logging.debug('''Going through __name__ == '__main__':''')
    pass
