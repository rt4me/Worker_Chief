# import requests
# import os
# import datetime
# import logging
# from dotenv import load_dotenv
# import format_reg_info_based_on_source
#
# load_dotenv()

#No longer used; placed this functionality in build_participant_dict.py file

test_event_number = 4
test_event_year = 2022


#Calendar GET request: https://api.motorsportreg.com/rest/calendars/organization/{{Organization_id}}.json
#Segment (work assignments) GET request: https://api.motorsportreg.com/rest/events/{{EventID}}/segments.json
#List Attendies (full list) GET request: https://api.motorsportreg.com/rest/events/{{EventID}}/attendees.json
#Registration (full list) GET request: https://api.motorsportreg.com/rest/events/{{EventID}}/assignments.json
#Entry List (I think this is the actual checked-in list) GET request: https://api.motorsportreg.com/rest/events/{{EventID}}/entrylist.json

# def get_event_uri(event_num, year = datetime.datetime.now().year):
#     '''sent request the MSR calendar for SCCA and return the ID of the first event listed. Incoming variables are for the Event number and year requested'''
#
#     logging.info('Entering get_event_id to query MSR API calendar to get the Event URI/ID')
#     logging.debug(f'Event number being used to query MSR API Calendar: {event_num}; Events year being used = {year}')
#
#     page = requests.get(f'https://api.motorsportreg.com/rest/calendars/organization/{os.getenv("ORGANIZATION_ID")}.json?start={year}-01-01&end={year}-12-31')
#     page_json = page.json()
#     events_list = page_json['response']['events']
#
#     logging.debug(f'Number of entries in calendar event list: {len(events_list)}')
#     logging.debug(f'Event List dump (1st Element): {events_list[1]}')
#
#
#     idx = 0
#     for x in events_list:
#         if f' E{event_num}' in x['name']:
#             event_uri = page_json['response']['events'][idx]['id']
#
#             logging.debug(f'Leaving get_event_id; Returning: {event_uri}')
#
#             return event_uri
#         idx += 1
#         logging.debug(f'Incrementing index number to {idx}')
#
#     logging.error(f'Information not found for event {event_num} in {year}')
#     logging.info('Leaving get_event_id')
#
#     return "Event not found!"
#
#
#
#
# def get_reg_assignments(event_uri):
#     '''Requests the assignment list for a provided event ID'''
#
#     logging.info('Entering get_reg_assignments')
#     logging.debug(f'Event ID being used to get registrations: {event_uri}')
#
#     url = f'https://api.motorsportreg.com/rest/events/{event_uri}/assignments.json'
#     logging.debug(f'URL being used: {url}')
#
#
#     response = requests.get(
#         url,
#         headers={
#             "X-Organization-Id": os.getenv('ORGANIZATION_ID'),
#             "Authorization": f'Basic {os.getenv("ENCODED_AUTHORIZATION")}'
#         },
#     )
#
#     logging.info(f'get_registration requests Response Code: {response.status_code}')
#
#     response_json = response.json()
#
#     logging.info('Leaving get_reg_assignments')
#     logging.debug(f'''get_reg_assignments is returning {response_json['response']['assignments']}''')
#
#     return 'API', response_json['response']['assignments']
#
# test_formatted_participan_list = format_reg_info_based_on_source.determin_reg_list_src(get_reg_assignments(get_event_uri(test_event_number, test_event_year)))
# print(f'Full Reg List: {get_reg_assignments(get_event_uri(test_event_number, test_event_year))}')
# print(test_formatted_participan_list)
# print('List of unique work assignments: {}'.format({participant.work_assign for participant in test_formatted_participan_list}))
# print('List of workers: {}'.format({(participant.fname + ' ' + participant.lname + ' : ' + participant.work_assign) for participant in test_formatted_participan_list if participant.work_req == 'Tech'}))

#print(f'Returned from get_event_id: {get_event_uri(test_event_number, test_event_year)}')
# print(f'Organization ID: {os.getenv("ORGANIZATION_ID")}')
#print(get_reg_assignments(get_event_uri(test_event_number, test_event_year)))