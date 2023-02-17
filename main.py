
import format_reg_info_based_on_source
import msr_api_reg_get
import file_reg_get
import logging

#Set Logging Level to print out
logging.basicConfig(
    level = logging.INFO,
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
MEDICAL_FILE = 'DataFiles/Medical.txt'
COURSE_SETUP_WORKERS = 'DataFiles/Course_Setup.txt'


#------------Use for checking API based process-------------------
event_id = msr_api_reg_get.get_event_id(3, 2022)
reg_list_api = msr_api_reg_get.get_registrations(event_id)
participant_list = format_reg_info_based_on_source.determin_reg_list_src(reg_list_api)
#Sort participant_list by Last Name
participant_list_sorted = sorted(participant_list, key=lambda x: x.__dict__['lname'])

print(f'Participant list sorted by Last Name: {participant_list_sorted}')


novice_cnt = 0
for x in participant_list_sorted:
    #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
    if x.__dict__['car_class'][0] == 'N':
        novice_cnt += 1
        print(x)
print(f'Novice count = {novice_cnt}')


#------------------Use for checking file based process--------------------
# reg_list_file = file_reg_get.read_ax_reg()
#
# for x in format_reg_info_based_on_source.determin_reg_list_src(reg_list_file):
#     #Return list of participants that have an 'N' in the first position of the class (i.e. Novices)
#     if x.__dict__['car_class'][0] == 'N':
#         print(x)


# def read_AXClassList(filename = AX_CLASS_LIST):
#     logging.info('Entring read_AXClassList')
#     with open(filename, 'r') as f:
#         lines_list = f.readlines()
#         for line in lines_list:
#             print(line.strip())







# print(f'List of people requesting to work Set Up: {find_requested_course_setup(read_ax_reg())}')
# print(f'List of unapproved setup workers: {find_invalid_setup_workers(read_ax_reg(), read_course_setup())}')
#print(f'List of unapproved setup workers: {find_invalid_setup_workers(reg_list, read_course_setup())}')

# if __name__ == '__main__':
#     main()
