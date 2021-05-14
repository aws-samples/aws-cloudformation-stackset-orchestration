import os
import json
from datetime import datetime
from botocore.stub import Stubber
import app as code
from test_events.test_event import test_event

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def test_trigger_step_function(monkeypatch):
    """
    Given an account configuration object is pushed to an s3 bucket
    When the handler is called
    Then a step function is triggered, with the account configuration object contents as the step functions input
    """
    # Given
    monkeypatch.setenv("STATE_MACHINE", "step_function_test_arn")
    s3_object_mock_content = open(
            os.path.join(__location__, "test_files/sample_account.yaml"),
            "r"
    ).read()
    s3_expected_params = {"Bucket": "test-bucket", "Key": "test-key" }
    s3_response = { "Body": s3_object_mock_content }
    step_functions_expected_input = {
        "account": "123456789876",
        "stacksets": [
            {
                "name": "vpc",
                "parameters": {
                    "CidrBlock": "10.0.0.0/24",
                    "EnableDnsHostnames":  "true"
                },
                "account": "123456789876"
            }
        ]
    }
    step_functions_expected_params = {
            "stateMachineArn": "step_function_test_arn",
            "input": json.dumps(step_functions_expected_input)
    }
    step_functions_response = {
            "executionArn": "execution_arn",
            "startDate": datetime(2010, 1, 1),
    }
    ## S3 mock configuration
    s3 = Stubber(code.s3)
    s3.add_response("get_object", s3_response, s3_expected_params)
    # Step Functions mock configuration
    step_functions = Stubber(code.step_functions)
    step_functions.add_response(
            "start_execution",
            step_functions_response,
            step_functions_expected_params
    )
    s3.activate()
    step_functions.activate()
    # When
    response = code.lambda_handler(test_event, {})
    s3.deactivate()
    step_functions.deactivate()
    # Then
    assert response == "execution_arn"

def test_trigger_step_function_terminate(monkeypatch):
    """
    Given an account configuration object with the terminate field set to True is pushed to an s3 bucket
    When the handler is called
    Then a step function is triggered, with the account configuration object contents as the step functions input
    """
    # Given
    monkeypatch.setenv("STATE_MACHINE", "step_function_test_arn")
    ## S3 mock configuration
    s3_object_mock_content = open(
            os.path.join(__location__, "test_files/sample_account_terminate.yaml"),
            "r"
    ).read()
    step_functions_expected_input = {
        "account": "123456789876",
        "terminate": True,
        "stacksets": [
            {
                "name": "vpc",
                "parameters": {
                    "CidrBlock": "10.0.0.0/24",
                    "EnableDnsHostnames":  "true"
                },
                "account": "123456789876",
                "terminate": True
            }
        ]
    }
    s3 = Stubber(code.s3)
    s3_expected_params = {"Bucket": "test-bucket", "Key": "test-key" }
    s3_response = { "Body": s3_object_mock_content }
    s3.add_response("get_object", s3_response, s3_expected_params)
    # Step Functions mock configuration
    step_functions = Stubber(code.step_functions)
    step_functions_expected_params = {
            "stateMachineArn": "step_function_test_arn",
            "input": json.dumps(step_functions_expected_input)
    }
    step_functions_response = {
            "executionArn": "execution_arn",
            "startDate": datetime(2010, 1, 1),
    }
    step_functions.add_response(
            "start_execution",
            step_functions_response,
            step_functions_expected_params
    )
    s3.activate()
    step_functions.activate()
    # When
    response = code.lambda_handler(test_event, {})
    s3.deactivate()
    step_functions.deactivate()
    # Then
    assert response == "execution_arn"
