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
import os
import json
import time
from random import randrange

cloudformation = boto3.client('cloudformation')

class StacksetCreationError(Exception):
   pass

def check_stackset_instance_for_errors(stackset_instance):

    if "StatusReason" in stackset_instance:
        stackset_instance_status = stackset_instance["Status"]
        stackset_instance_status_reason = stackset_instance["StatusReason"]

        # Raise exception if there is an error while creating the stackset instance
        if stackset_instance_status == "OUTDATED" and "Error" in stackset_instance_status_reason:
            raise StacksetCreationError(stackset_instance_status_reason)

def stackset_instance_ready(stackset_name, account_id, region):

    # Add jitter
    time.sleep(randrange(10,20))
    # Get stackset instance information
    stackset_instance = cloudformation.list_stack_instances(
                                StackSetName=stackset_name,
                                StackInstanceAccount=account_id,
                                StackInstanceRegion=region)
    print("Recovered stacket instance: ")
    print(stackset_instance)

    stackset_instance = stackset_instance["Summaries"][0]

    # Check for errors in stackset instance creation
    check_stackset_instance_for_errors(stackset_instance)

    stackset_instance_status = stackset_instance["Status"]

    return True if stackset_instance_status == "CURRENT" else False


def lambda_handler(event, context):
    region = os.environ["AWS_REGION"]
    # Wait for stackset instance creation
    print("Waiting for stackset instance to be processed...")
    time.sleep(30)
    # Get stackset instance information
    print("Received event: " + json.dumps(event, indent=2))
    stackset_instance = event["stackset_instance_in_treatment"]
    terminate_stack_instance = event["terminate"] if "terminate" in event else False
    stackset_name = stackset_instance["name"]
    account_id = str(stackset_instance["account_id"])
    print("StackSet instance: " + json.dumps(stackset_instance, indent=2))
    print("StackSet Name: " + stackset_name)
    print("AccountId: " + account_id)

    # Update stackset instance status, or fail the pipeline if there is an error
    try:
        event["stackset_instance_ready"] = True if terminate_stack_instance else stackset_instance_ready(stackset_name, account_id, region)
    except StacksetCreationError as e:
        print("StacksetCreationError")
        print(e)
        raise e

    print("Outgoing event: " + json.dumps(event, indent=2))

    return event
