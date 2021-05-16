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

import json
import os
import urllib.parse

import boto3
import yaml

s3 = boto3.client("s3")
step_functions = boto3.client("stepfunctions")

STATE_MACHINE_ARN = os.getenv("STATE_MACHINE")


def get_config_file(event):
    # Get event parameters
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    # Get object config file
    try:
        config_file = s3.get_object(Bucket=bucket, Key=key)
    except Exception as e:
        print(e)
        raise e
    return config_file


def parse(config_file):
    # Parse yaml file
    try:
        parsed_config_file = yaml.safe_load(config_file["Body"])
    except yaml.YAMLError as exc:
        return exc
    return parsed_config_file


def add_account_information(config_file):
    for stackset in config_file["stacksets"]:
        stackset["account"] = config_file["account"]
        if "terminate" in config_file and config_file["terminate"]:
            stackset["terminate"] = config_file["terminate"]
    return config_file


def trigger_step_function(config_file):
    # Start step function
    print(
        "Trigerring Step functions with these values: "
        + json.dumps(config_file, indent=2)
    )
    response = step_functions.start_execution(
        stateMachineArn=STATE_MACHINE_ARN, input=json.dumps(config_file)
    )
    return response


def lambda_handler(event, context):
    config_file = get_config_file(event)
    config_file = parse(config_file)
    config_file = add_account_information(config_file)
    response = trigger_step_function(config_file)
    return response["executionArn"]
