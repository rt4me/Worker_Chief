import logging

def find_requested_course_setup(reg_list):
    '''Take in the output of the read_ax_reg and returns all participants that requested to work course setup'''

    logging.info('Entering find_requested_course_setup')
    logging.debug(f'Setting up empty requested_setup_list inside read_ax_reg.')

    requested_setup_list = []
    for x in read_ax_reg(REG_FILE):
        if x['Group'] == 'Course Set Up':
            requested_setup_list.append(f'''{x['First Name']} {x['Last Name']}''')

    logging.info('Leaving find_requested_course_setup')
    logging.debug(f'Returning requested_setup_list: {requested_setup_list}')

    return requested_setup_list



def read_course_setup(filename = COURSE_SETUP_WORKERS):
    '''Read provided filename (should be Locked_work_assignments.txt) to get the official list of Course Setup workers'''
    logging.info('Entering read_course_setup')
    logging.debug(f'Setting up empty official_setup_workers list inside read_course_setup.')

    official_setup_workers = []
    with open(filename, 'r') as f:
        lines_list = f.readlines()
        for line in lines_list:
            official_setup_workers.append(line.strip())

    logging.info('Leaving read_course_setup')
    logging.debug(f'Returning official_setup_workers: {official_setup_workers}')

    return official_setup_workers


def find_invalid_setup_workers(reg_list = read_ax_reg, approved_setup_list = read_course_setup()):
    '''Compare the full registration list  to see who requested to work Course Set Up but aren't on the official Set Up List'''

    logging.info('Entering find_invalid_setup_workers')
    logging.debug(f'find_invalid_setup_workers: Incoming approved course setup list: {approved_setup_list}')
    #logging.debug(f'find_invalid_setup_workers: Incoming registration list: {reg_list}')
    logging.debug(f'Setting up empty unapproved_setup_workers inside read_ax_reg.')

    unapproved_setup_workers = []
    for x in reg_list:
        if x['Group'] == 'Course Set Up' and f'''{x['First Name']} {x['Last Name']}''' not in approved_setup_list:
            unapproved_setup_workers.append(f'''{x['First Name']} {x['Last Name']}''')

    logging.info('Leaving find_invalid_setup_workers')
    logging.debug(f'Returning unapproved_setup_workers: {unapproved_setup_workers}')

    return unapproved_setup_workers