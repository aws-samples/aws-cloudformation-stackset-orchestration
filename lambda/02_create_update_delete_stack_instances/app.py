# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import boto3
import time
import os
from random import randrange

cloudformation = boto3.client('cloudformation')
region = os.environ["AWS_REGION"]

def format_parameters(parameters):
    formatted_parameters = []
    for key, value in parameters.items():
        formatted_parameters.append({
            "ParameterKey": key,
            "ParameterValue": value
        })
    return formatted_parameters

def stackinstance_exists(stackset_name, account_id, region):
    # Add jitter
    time.sleep(randrange(10,20))
    stack_instance_size = len(cloudformation.list_stack_instances(
                                StackSetName=stackset_name,
                                StackInstanceAccount=account_id,
                                StackInstanceRegion=region)["Summaries"]
    )
    return True if stack_instance_size > 0 else False


def lambda_handler(event, context):
    # Get stackset instance information
    account_id = str(event["account"])
    terminate_stack_instance = event["terminate"] if "terminate" in event else False
    stackset_name = event["name"]
    parameter_overrides = format_parameters(event["parameters"]) if "parameters" in event else []

    # Check if the operation is create, update or delete
    if terminate_stack_instance:
        operation_function = cloudformation.delete_stack_instances
        operation_arguments = {
                "StackSetName": stackset_name,
                "Accounts":[ account_id ],
                "RetainStacks": False,
                "Regions":[ region ]
        }
    else:
        operation_function = cloudformation.update_stack_instances if stackinstance_exists(stackset_name, account_id, region) else cloudformation.create_stack_instances
        operation_arguments = {
                "StackSetName": stackset_name,
                "Accounts": [ account_id ],
                "ParameterOverrides": parameter_overrides,
                "Regions": [ region ]
        }

    # Add jitter
    time.sleep(randrange(10,20))
    # Perform operation
    response = operation_function(**operation_arguments)
    print(response)

    # Update stackset instance in creation data
    event["stackset_instance_in_treatment"] = {
            "name": stackset_name,
            "account_id": account_id
    }

    return event
