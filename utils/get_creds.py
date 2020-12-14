import boto3
import os
import sys

sys.path.append(os.getcwd())

region = "eu-west-2"
output_file = "./build.properties"
aws_profile_name = os.environ.get("AWS_PROFILE_NAME", "hmpps-token")
aws_role_arn = os.environ.get(
    "AWS_ROLE_ARN", "arn:aws:iam::895523100917:role/terraform")

session = boto3.Session(profile_name=aws_profile_name)

sts_client = session.client("sts")
assumed_role_object = sts_client.assume_role(
    RoleArn=aws_role_arn,
    RoleSessionName="PackerSession"
)

credentials = assumed_role_object["Credentials"]
access_key_id = credentials["AccessKeyId"]
secret_access_key = credentials["SecretAccessKey"]
session_token = credentials["SessionToken"]

bash_data = f"""#!/usr/bin/env bash
export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}
export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}
export AWS_SESSION_TOKEN={credentials['SessionToken']}
export AWS_ACCESS_KEY={credentials['AccessKeyId']}
export AWS_SECRET_KEY=={credentials['SecretAccessKey']}
export AWS_SECURITY_TOKEN={credentials['SessionToken']}
export AWS_DEFAULT_REGION={region}
"""

with open(output_file, "w") as build:
    build.write(bash_data)
