
import format_reg_info_based_on_source
import msr_api_reg_get
import file_reg_get
import logging
import csv

#Set Logging Level to print out
logging.basicConfig(
    level = logging.INFO, #Levels are DEBUG, INFO, WARNING, ERROR and CRITICAL
    format = '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    #,filename = 'basic.log'
)

# logging.debug('This is a debug message.')
# logging.info('This is an info message.')
# logging.warning('This is a warning message.')
# logging.error('This is an error message.')
# logging.critical('This is a critical message.')

AX_CLASS_LIST = 'DataFiles/AXClassList.txt'
AX_CLASS_MODIFIER_LIST = 'DataFiles/AXClassModifiers.txt'
MEDICAL_FILE = 'DataFiles/Medical.txt'
COURSE_SETUP_WORKERS = 'DataFiles/Course_Setup.txt'


#------------Use for checking API based process-------------------
event_id = msr_api_reg_get.get_event_id(3, 2022)
reg_list_api = msr_api_reg_get.get_registrations(event_id)
participant_list = format_reg_info_based_on_source.determin_reg_list_src(reg_list_api)

#Sort participant_list by Last Name
participant_list_sorted = sorted(participant_list, key=lambda x: x.__dict__['lname'])

#print(f'Participant list sorted by Last Name: {participant_list_sorted}')


def novice_list_and_count(participant_list = participant_list):
    novice_cnt = 0
    novice_list = []
    for x in participant_list:
        #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
        if x.__dict__['car_class'][0] == 'N':
            novice_cnt += 1
            novice_list.append(x)
    return(novice_cnt, novice_list)

print(f'''Count of Novices: {novice_list_and_count()[0]}, Novice List: {novice_list_and_count()[1]}''')

#------------------------------------------Use for checking file based process---------------------------------------------
# reg_list_file = file_reg_get.read_ax_reg()
#
# for x in format_reg_info_based_on_source.determin_reg_list_src(reg_list_file):
#     #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
#     if x.__dict__['car_class'][0] == 'N':
#         print(x)






#---------------------------------------------Build Complete AX Class List----------------------------------------------------
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

# if __name__ == '__main__':
#     main()
