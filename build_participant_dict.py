import requests
import os
import datetime
import logging
import csv
from dotenv import load_dotenv
import participant

load_dotenv()


#=========================================================================================================
#
#      This section is related to doing a GET on the MSR API to get assignment information.
#
#=========================================================================================================

def get_event_uri(event_num, year = datetime.datetime.now().year):
    '''sent request the MSR calendar for SCCA and return the ID of the first event listed.
    Incoming variables are for the Event number and year requested'''

    logging.info('Entering get_event_id to query MSR API calendar to get the Event URI/ID')
    logging.debug(f'Event number being used to query MSR API Calendar: {event_num}; Events year being used = {year}')

    page = requests.get(f'https://api.motorsportreg.com/rest/calendars/organization/{os.getenv("ORGANIZATION_ID")}.json?start={year}-01-01&end={year}-12-31')
    page_json = page.json()
    events_list = page_json['response']['events']

    logging.debug(f'Number of entries in calendar event list: {len(events_list)}')
    logging.debug(f'Event List dump (1st Element): {events_list[1]}')


    idx = 0
    for x in events_list:
        if f' E{event_num}' in x['name']:
            event_uri = page_json['response']['events'][idx]['id']

            logging.debug(f'Leaving get_event_id; Returning: {event_uri}')

            return event_uri
        idx += 1
        logging.debug(f'Incrementing index number to {idx}')

    logging.error(f'Information not found for event {event_num} in {year}')
    logging.info('Leaving get_event_id')

    return "Event not found!"




def get_reg_assignments(event_uri):
    '''Requests the assignment list for a provided event ID'''

    logging.info('Entering get_reg_assignments')
    logging.debug(f'Event ID being used to get registrations: {event_uri}')

    url = f'https://api.motorsportreg.com/rest/events/{event_uri}/assignments.json'
    logging.debug(f'URL being used: {url}')


    response = requests.get(
        url,
        headers={
            "X-Organization-Id": os.getenv('ORGANIZATION_ID'),
            "Authorization": f'Basic {os.getenv("ENCODED_AUTHORIZATION")}'
        },
    )

    logging.info(f'get_registration requests Response Code: {response.status_code}')

    response_json = response.json()

    logging.info('Leaving get_reg_assignments')
    logging.debug(f'''get_reg_assignments is returning {response_json['response']['assignments']}''')

    return 'API', response_json['response']['assignments']



#=========================================================================================================
#
#      This section is related to reading registration information from a "worker chief" report csv file.
#      Only used if the API code above is not used or available.
#
#=========================================================================================================

#reg_file = 'DataFiles/20200531-WorkerAssignment.csv'

def get_reg_file_path():
    logging.debug('Asking for user to enter file name and path for Worker Sheet Report')
    worker_assign_report = input('Enter path/name of Worker Assignment sheet (defaults to hard coded value): ') or 'DataFiles/20200531-WorkerAssignment.csv'
    logging.info(f'file entry value: {worker_assign_report}')
    return worker_assign_report

def read_ax_reg_file(filename = get_reg_file_path()):
    '''Read the WorkerAssignment csv file. Build a list of dictionaries from this information.
    Not needed if reading data from the get_reg_assignments API call'''

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




#=========================================================================================================
#
#      This section is related to ...
#
#=========================================================================================================


#The below functionality was moved to the main.py file.
# def determin_reg_list_src(reader_response):
#     '''Function pulls the first element from the response of either the read_reg_file or msr_app_reg_get classes to see where data was sourced from.
#     Expected values are FILE or API. Depending on which value is found, it will sent the payload to the appropriate function to reformat to standard Participant data class'''
#     if reader_response[0] == 'FILE':
#         logging.info('Processing registration reformat based on FILE source')
#         return(data_source_from_file(reader_response[1]))
#     elif reader_response[0] == 'API':
#         logging.info('Processing registration reformat based on API source')
#         return(data_source_from_api(reader_response[1]))
#     else:
#         logging.info('Registration source not recognized as FILE or API')
#         return('Registration source not recognized as FILE or API')


def data_source_from_file(reg_list):
    '''Incoming list of dictionaries is expected to be sourced from a "worker chief" csv report file exported from MSR
    From that, a list of Participant Data Class instances will be build and returned.'''

    logging.debug(f'data_source_from_file(reg_list) coming in: {reg_list}')

    participant_list = []
    for x in reg_list:

        logging.debug(f'Element being processed in for loop for x = {x}')

        prtcpnt = participant.Participant(
            fname = x['First Name'],
            lname = x['Last Name'],
            car_class = x['Class + Modifier/PAX'],
            car_num = x['No.'],
            work_req= x['Group'],
            member_id = x['Member #']
        )

        logging.debug(f'Adding the following participant to participant_list: {prtcpnt}')

        participant_list.append(prtcpnt)
    logging.info(f'Exiting format_reg_info_based_on_source.data_source_from_file')
    logging.debug(f'Returning the following list: {participant_list}')

    return participant_list



def data_source_from_api(reg_list):
    '''Incoming list of dictionaries is expected to be sourced from response of a GET to the MSR API'''
    logging.debug(f'data_source_from_file(reg_list) coming in: {reg_list[100]}')

    participant_list = []
    for x in reg_list:

        logging.debug(f'Element being processed in for loop for x = {x}')

        prtcpnt = participant.Participant(
            fname=x['firstName'],
            lname=x['lastName'],
            car_class=x['classShort']+x['classModifierShort'],
            car_num=x['vehicleNumber'],
            work_req=x['groupShort'],
            member_id=x['memberId']
        )
        logging.debug(f'Adding participant: {prtcpnt}')

        participant_list.append(prtcpnt)
    logging.info(f'Exiting format_reg_info_based_on_source.data_source_from_file')
    logging.debug(f'Returning the following list: {participant_list}')

    return participant_list


#API based test area:
# test_formatted_participan_list = format_reg_info_based_on_source.determin_reg_list_src(get_reg_assignments(get_event_uri(test_event_number, test_event_year)))
# print(f'Full Reg List: {get_reg_assignments(get_event_uri(test_event_number, test_event_year))}')
# print(test_formatted_participan_list)
# print('List of unique work assignments: {}'.format({participant.work_assign for participant in test_formatted_participan_list}))
# print('List of workers: {}'.format({(participant.fname + ' ' + participant.lname + ' : ' + participant.work_assign) for participant in test_formatted_participan_list if participant.work_req == 'Tech'}))

#print(f'Returned from get_event_id: {get_event_uri(test_event_number, test_event_year)}')
# print(f'Organization ID: {os.getenv("ORGANIZATION_ID")}')
#print(get_reg_assignments(get_event_uri(test_event_number, test_event_year)))


if __name__ == '__main__':
    logging.debug('''Going through __name__ == '__main__':''')
    pass