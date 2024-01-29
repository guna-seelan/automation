import pytest
from pytest_bdd import given, then, when, scenario
from custom_logger import logger
import os,json,requests,uuid

from test.pytestbdd.tests import create_json

# from okta_pkce.newORGOktaToken import login

# load config json
with open('config.json') as file:
    localSettings = json.load(file)

for i in localSettings['data']:
    os.environ[i] = localSettings['data'][i]

local_path = '../test-data/test_update_org_invalid/'

scenario_name = "Org does not exist"

@scenario('test_Update_invalid_org.feature', str(scenario_name))
def test_Update_invalid_org():
    pass
@given('User is having updated contract information available')
def prepare_authorization_token():
    logger.info('Step:1')
    global json_data
    try:
        with open(local_path+"org_update_invalid.json", 'r') as data:
            base_data = json.load(data)
        base_json = json.dumps(base_data)
        id = str(uuid.uuid4())
        string_data=base_json.replace("{uuid}", id)
        json_data = json.loads(string_data)
        logger.info(f"Updated contract information is :{json_data['contract']} ")
        test_status = True
    except Exception as e:
        logger.error(e)
        test_status = False
    assert test_status

@when('User makes call to Org API to update the organization')
def prepare_for_org_payload():
    logger.info('Step:2')
    try:
        logger.info(f"Organization API url to update the organization is : {os.environ['org_api_url']}")
        test_status = True
    except Exception as e:
        logger.error(e)
        test_status = False
    assert test_status

@when('Specify fields (Org ID, Org Name, Contract details) that needs to be updated')
def verify_basic_information():
    logger.info('Step:3')
    try:
        logger.info(f"Fields specified to update organization is : Org ID, Org Name, Contract details")
        test_status = True
    except Exception as e:
        logger.error(e)
        test_status = False
    assert test_status

@then('System shall error out the request')
def verify_status_code():
    logger.info('Step:4')
    global response,base_url
    try:
        # logger.info("Retrieving Organization API url from configuration file and creating authorization token using OKTA.")
        headers = {
            "Authorization": os.environ["valid_okta_token"],
            'User-Agent': 'PostmanRuntime/7.29.2',
            'Content-Type': 'application/json'}
        base_url = f'{os.environ["org_api_url"]}/{os.environ["invalid_org_id"]}'
        response = requests.put(base_url,headers=headers, data=json.dumps(json_data))
        response_code = response.status_code
        logger.info(f"Status code from the response is : {response_code}")
        assert response_code == 404
        test_status = True
    except Exception as e:
        logger.error(e)
        test_status = False
    assert test_status

@then('Notify user that org does not exist')
def verify_error_message():
    logger.info('Step:5')
    result_data = response.json()
    error_message = result_data['errors'].split(":")[0].strip()
    logger.info(f"Response for 'Org does not exist' is : {error_message}")
    assert error_message == "Organization does not exist"
    evidence = "evidence"
    create_json.createjson(scenario_name, evidence)

