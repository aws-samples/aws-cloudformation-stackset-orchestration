from botocore.stub import Stubber
import app as code


def test_verify_create_update_not_ready(monkeypatch):
    """
    Given a setup function input for verifying stack instances, when the stackset instance is not ready
    When the handler is called
    Then handler return a dict with the stackset_instance_ready variable set to False
    """
    # Given
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    monkeypatch.setattr(code.time, "sleep", lambda _: None)
    stackset_name = "vpc"
    account_id = "123456789876"
    region = "eu-west-1"
    parameters = {
        "CidrBlock": "10.0.0.0/24",
        "EnableDnsHostnames": "true"
    }
    step_function_input = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        }
    }
    step_function_expected_output = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        },
        "stackset_instance_ready": False
    }
    cloudformation_list_expected_params = {
            "StackSetName": stackset_name,
            "StackInstanceAccount": account_id,
            "StackInstanceRegion": region
    }
    cloudformation_list_response = {
        "Summaries": [
            {
                "StackSetId": "vpc:stackset-id",
                "Region": region,
                "Account": account_id,
                "Status": "OUTDATED",
                "StatusReason": "StatusReason",
                "StackInstanceStatus": {
                    "DetailedStatus": "SUCCESS"
                },
                "OrganizationalUnitId": "",
                "DriftStatus": "NOT_CHECKED"
            }
        ]
    }
    ## Cloudformation mock configuration
    cloudformation = Stubber(code.cloudformation)
    cloudformation.add_response(
            "list_stack_instances",
            cloudformation_list_response,
            cloudformation_list_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == step_function_expected_output


def test_verify_create_update_ready(monkeypatch):
    """
    Given a setup function input for verifying stack instances, when the stackset instance is ready
    When the handler is called
    Then handler return a dict with the stackset_instance_ready variable set to True
    """
    # Given
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    monkeypatch.setattr(code.time, "sleep", lambda _: None)
    stackset_name = "vpc"
    account_id = "123456789876"
    region = "eu-west-1"
    parameters = {
        "CidrBlock": "10.0.0.0/24",
        "EnableDnsHostnames": "true"
    }
    step_function_input = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        }
    }
    step_function_expected_output = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        },
        "stackset_instance_ready": True
    }
    cloudformation_list_expected_params = {
            "StackSetName": stackset_name,
            "StackInstanceAccount": account_id,
            "StackInstanceRegion": region
    }
    cloudformation_list_response = {
        "Summaries": [
            {
                "StackSetId": "vpc:stackset-id",
                "Region": region,
                "Account": account_id,
                "Status": "CURRENT",
                "StatusReason": "StatusReason",
                "StackInstanceStatus": {
                    "DetailedStatus": "SUCCESS"
                },
                "OrganizationalUnitId": "",
                "DriftStatus": "NOT_CHECKED"
            }
        ]
    }
    ## Cloudformation mock configuration
    cloudformation = Stubber(code.cloudformation)
    cloudformation.add_response(
            "list_stack_instances",
            cloudformation_list_response,
            cloudformation_list_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == step_function_expected_output


def test_verify_delete(monkeypatch):
    """
    Given a setup function input for verifying the deletion stack instances
    When the handler is called
    Then handler return a dict with the stackset_instance_ready variable set to True
    """
    # Given
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    monkeypatch.setattr(code.time, "sleep", lambda _: None)
    stackset_name = "vpc"
    account_id = "123456789876"
    region = "eu-west-1"
    parameters = {
        "CidrBlock": "10.0.0.0/24",
        "EnableDnsHostnames": "true"
    }
    step_function_input = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "terminate": True,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        }
    }
    step_function_expected_output = {
        "name": stackset_name,
        "parameters": parameters,
        "account": account_id,
        "terminate": True,
        "stackset_instance_in_treatment": {
            "name": stackset_name,
            "account_id": account_id
        },
        "stackset_instance_ready": True
    }
    cloudformation_list_expected_params = {
            "StackSetName": stackset_name,
            "StackInstanceAccount": account_id,
            "StackInstanceRegion": region
    }
    cloudformation_list_response = {
        "Summaries": [
            {
                "StackSetId": "vpc:stackset-id",
                "Region": region,
                "Account": account_id,
                "Status": "OUTDATED",
                "StatusReason": "StatusReason",
                "StackInstanceStatus": {
                    "DetailedStatus": "SUCCESS"
                },
                "OrganizationalUnitId": "",
                "DriftStatus": "NOT_CHECKED"
            }
        ]
    }
    ## Cloudformation mock configuration
    cloudformation = Stubber(code.cloudformation)
    cloudformation.add_response(
            "list_stack_instances",
            cloudformation_list_response,
            cloudformation_list_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == step_function_expected_output
