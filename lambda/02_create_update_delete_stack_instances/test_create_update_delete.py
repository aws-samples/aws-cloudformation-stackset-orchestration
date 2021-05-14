from botocore.stub import Stubber
import app as code


def test_handler_create(monkeypatch):
    """
    Given a setup function input for creating stack instances
    When the handler is called
    Then the CreateStackInstances action of the CloudFormation API is called with the stackset parameters
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
    parameter_overrides = [
        {
            "ParameterKey": "CidrBlock",
            "ParameterValue": "10.0.0.0/24"
        },{
            "ParameterKey": "EnableDnsHostnames",
            "ParameterValue": "true"
        }
    ]
    step_function_input = {
      "name": stackset_name,
      "parameters": parameters,
      "account": account_id,
    }
    expected_step_function_output = {
      "name": stackset_name,
      "parameters": parameters,
      "account": account_id,
      "stackset_instance_in_treatment": {
          "name": stackset_name,
          "account_id": account_id
      }
    }
    cloudformation_create_expected_params = {
            "StackSetName": stackset_name,
            "Accounts":[ account_id ],
            "ParameterOverrides": parameter_overrides,
            "Regions":[ region ]
    }
    cloudformation_create_response = {
            "OperationId": "operation-id"
    }
    cloudformation_list_expected_params = {
            "StackSetName": stackset_name,
            "StackInstanceAccount": account_id,
            "StackInstanceRegion": region
    }
    cloudformation_list_response = {
        "Summaries": []
    }
    ## Cloudformation mock configuration
    cloudformation = Stubber(code.cloudformation)
    cloudformation.add_response(
            "list_stack_instances",
            cloudformation_list_response,
            cloudformation_list_expected_params
    )
    cloudformation.add_response(
            "create_stack_instances",
            cloudformation_create_response,
            cloudformation_create_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == expected_step_function_output


def test_handler_update(monkeypatch):
    """
    Given a setup function input for updating stack instances
    When the handler is called
    Then the UpdateStackInstances action of the CloudFormation API is called with the stackset parameters
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
    parameter_overrides = [
        {
            "ParameterKey": "CidrBlock",
            "ParameterValue": "10.0.0.0/24"
        },{
            "ParameterKey": "EnableDnsHostnames",
            "ParameterValue": "true"
        }
    ]
    step_function_input = {
      "name": stackset_name,
      "parameters": parameters,
      "account": account_id,
    }
    expected_step_function_output = {
      "name": stackset_name,
      "parameters": parameters,
      "account": account_id,
      "stackset_instance_in_treatment": {
          "name": stackset_name,
          "account_id": account_id
      }
    }
    cloudformation_create_expected_params = {
        "StackSetName": stackset_name,
        "Accounts":[ account_id ],
        "ParameterOverrides": parameter_overrides,
        "Regions":[ region ]
    }
    cloudformation_create_response = {
        "OperationId": "operation-id"
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
    cloudformation.add_response(
            "update_stack_instances",
            cloudformation_create_response,
            cloudformation_create_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == expected_step_function_output


def test_handler_delete(monkeypatch):
    """
    Given a setup function input for updating stack instances
    When the handler is called
    Then the DeleteStackInstances action of the CloudFormation API is called with the stackset parameters
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
      "terminate": True
    }
    expected_step_function_output = {
      "name": stackset_name,
      "parameters": parameters,
      "account": account_id,
      "terminate": True,
      "stackset_instance_in_treatment": {
          "name": stackset_name,
          "account_id": account_id
      }
    }
    cloudformation_expected_params = {
            "StackSetName": stackset_name,
            "Accounts":[ account_id ],
            "RetainStacks": False,
            "Regions":[ region ]
    }
    cloudformation_response = {
            "OperationId": "operation-id"
    }
    ## Cloudformation mock configuration
    cloudformation = Stubber(code.cloudformation)
    cloudformation.add_response(
            "delete_stack_instances",
            cloudformation_response,
            cloudformation_expected_params
    )
    cloudformation.activate()
    # When
    response = code.lambda_handler(step_function_input, {})
    cloudformation.deactivate()
    # Then
    assert response == expected_step_function_output
