import logging
import participant

#Set Logging Level to print out
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(levelname)s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
    #,filename = 'basic.log'
)
partipant_list = []

def determin_reg_list_src(reader_response):
    '''Function pulls the first element from the response of either the read_reg_file or msr_app_reg_get classes to see where data was sourced from.
    Expected values are FILE or API. Depending on which value is found, it will sent the payload to the appropriate function to reformat to standard Participant data class'''
    if reader_response[0] == 'FILE':
        logging.info('Processing registration reformat based on FILE source')
        return(data_source_from_file(reader_response[1]))
    elif reader_response[0] == 'API':
        logging.info('Processing registration reformat based on API source')
        return(data_source_from_api(reader_response[1]))
    else:
        logging.info('Registration source not recognized as FILE or API')
        return('Registration source not recognized as FILE or API')


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