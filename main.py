import csv

AX_CLASS_LIST = 'AXClassList.txt'
REG_FILE = 'DataFiles/20200531-WorkerAssignment.csv'
MEDICAL_FILE = 'DataFiles/Medical.txt'
COURSE_SETUP_WORKERS = 'Course_Setup.txt'

def read_AXClassList(filename):
    with open(filename, 'r') as f:
        lines_list = f.readlines()
        for line in lines_list:
            print(line.strip())

def read_course_setup(filename):
    official_setup_workers = []
    with open(filename, 'r') as f:
        lines_list = f.readlines()
        for line in lines_list:
            official_setup_workers.append(line.strip())
    return official_setup_workers


def read_ax_reg(filename):
    '''Read the WorkerAssignment csv file. Build a list of dictionaries from this information'''
    reg_list = []
    with open(filename, newline = '') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reg_list.append(row)
    return reg_list

def find_requested_course_setup(reg_list):
    '''Take in the output of the read_ax_reg and returns all participants that requested to work course setup'''
    requested_setup_list = []
    for x in read_ax_reg(REG_FILE):
        if x['Group'] == 'Course Set Up':
            requested_setup_list.append(f'''{x['First Name']} {x['Last Name']}''')
    return requested_setup_list


def find_invalid_setup_workers(reg_list, approved_setup_list):
    '''Compare the full registration list  to see who requested to work Course Set Up but aren't on the official Set Up List'''
    unapproved_setup_workers = []
    for x in reg_list:
        if x['Group'] == 'Course Set Up' and f'''{x['First Name']} {x['Last Name']}''' not in approved_setup_list:
            unapproved_setup_workers.append(f'''{x['First Name']} {x['Last Name']}''')
    return unapproved_setup_workers


print(f'List of people requesting to work Set Up: {find_requested_course_setup(read_ax_reg(REG_FILE))}')
print(f'List of unapproved setup workers: {find_invalid_setup_workers(read_ax_reg(REG_FILE), read_course_setup(COURSE_SETUP_WORKERS))}')


# if __name__ == '__main__':
#     main()
