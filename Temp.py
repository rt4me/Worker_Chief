#Pulled from https://gist.github.com/g12r/e3f33f31fe0baca4f73b4612c0c21e71
import logging
import os
import requests
#Used to read .env file variables
from dotenv import load_dotenv
load_dotenv()

#Pulled from .env file setup
ORG_ID = os.getenv('ORGANIZATION_ID')
AUTHORIZATION = os.getenv('ENCODED_AUTHORIZATION')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _get_msr_endpoint(service_url):
    return "https://api.motorsportreg.com/rest/" + service_url


def get_request(url, params=None):
    # noinspection PyBroadException
    #print(f'url = {url}, ORG ID = {ORG_ID}, Authorization = {AUTHORIZATION}')
    try:
        response = requests.get(
            url,
            #params,
            headers={
                "X-Organization-Id": ORG_ID,
                "Authorization": f'Basic {AUTHORIZATION}', # can use HTTPBasicAuth(username, password)
            },
        )
        logger.debug("Response HTTP Status Code: %s", response.status_code)
        logger.debug("Response HTTP Response Body: %s", response.content)
        print(f'Response Status Code = {response.status_code}')
        return response.json()
    except requests.exceptions.RequestException:
        logger.error("HTTP Request failed")
    except:
        logger.error("Other exception!")


def get_events():
    url = _get_msr_endpoint(f"calendars/organization/{ORG_ID}.json")
    params = {"archive": "true"}
    result = get_request(url, params)
    return result["response"]


def get_member(member_id):
    url = _get_msr_endpoint(f"members/{member_id}.json")
    params = {"fields": "questions"}
    result = get_request(url, params)
    return result["response"]["member"]


def get_event_attendees_json(event_id):
    url = _get_msr_endpoint(f"events/{event_id}/attendees.json")
    params = {"fields": "questions"}
    result = get_request(url, params)
    return result


def get_event_attendees(event_id):
    url = _get_msr_endpoint(f"events/{event_id}/attendees.json")
    params = {"fields": "questions"}
    result = get_request(url, params)
    print(f'Get Event Attendees result: {result}')
    if "response" in result:
        if "attendees" in result["response"]:
            return result["response"]
        else:
            logger.error(
                f"Unexpected response returned, payload included 'response' but not 'attendees': event_id = {event_id}"
            )
            return None
    elif "error" in result:
        logger.error(f"Error returned: {result['error']}, event_id = {event_id}")
        return None
    else:
        logger.error(
            f"Unexpected response returned, payload did not include 'response' or 'error', event_id = {event_id}"
        )
        return None

#Provide Event ID value
get_event_attendees('316B11CB-EA97-C4CA-4559348420FC3626')