#!/usr/bin/env python3
"""
CloudFront CNAME Swap DNS Automation Script

Author: Trevor Henning (hthennin)

This script monitors a CloudFront distribution for a CNAME swap and automatically
updates the corresponding Route 53 DNS record to minimize downtime.

Usage:
    python3 cloudfront_dns_automation.py <new-distribution-id> <route53-hosted-zone-id> 
                                        <old-cloudfront-domain> <new-cloudfront-domain> 
                                        <alias-alternate-name>

Example:
    python3 cloudfront_dns_automation.py EZDLMTR1D3MHD Z00646902JW6C5QG3Q2NG 
                                        d2szizvz5rw5zj.cloudfront.net. 
                                        d2mz62fpvuge8k.cloudfront.net. 
                                        www.example.com
"""

import boto3 
import json
import sys

session = boto3.Session()
r53 = session.client('route53')
cf = session.client('cloudfront')
sts = session.client('sts') #to assume a role if needed

def checkAlias(cloudfrontID, alias):
    response = cf.get_distribution(Id=cloudfrontID)
    print(response["Distribution"]["DistributionConfig"]["Aliases"]["Items"])
    while (alias not in response["Distribution"]["DistributionConfig"]["Aliases"]["Items"]):
        response = cf.get_distribution(Id=cloudfrontID) 
    return True

def updateRecord(hostedzoneID, old_domain, new_domain, alias):
    #To assume a role to update a record or all an API in another account, please follow our guides here: 
    #https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-api.html 
     
    #For example, please see the below sample process to assume a role to make a call in Route 53
    #1. assume role 
    #sts_response = sts.assume_role(RoleArn="role-ARN-here", RoleSessionName="session-name-here")
    #temp_credentials = sts_response["Credentials"]

    #2. Create r53 resource w/ new credentials 
    #r53_resource = boto3.resource(
    #    "route53",
    #    aws_access_key_id=temp_credentials["AccessKeyId"],
    #    aws_secret_access_key=temp_credentials["SecretAccessKey"],
    #    aws_session_token=temp_credentials["SessionToken"],
    #)
    #3. Call the below call w/ new r53 resource, for ex: use r53_resource.change_resource_record_sets, instead of the below r53.change_resource_record_sets

    response = r53.change_resource_record_sets(
    HostedZoneId=hostedzoneID,
    ChangeBatch={
        'Comment': 'string',
        'Changes': [
            {
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': alias,
                    'Type': 'A',
                    'AliasTarget': {
                        'HostedZoneId': 'Z2FDTNDATAQYW2',
                        'DNSName': old_domain,
                        'EvaluateTargetHealth': False
                    }
                }
            },
                        {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': alias,
                    'Type': 'A',
                    'AliasTarget': {
                        'HostedZoneId': 'Z2FDTNDATAQYW2',
                        'DNSName':new_domain,
                        'EvaluateTargetHealth': False
                    }
                }
            },
        ]
    }
)


def main():
    cloudfrontID = sys.argv[1]
    hostedzoneID = sys.argv[2]
    old_domain = sys.argv[3]
    new_domain = sys.argv[4]
    alias = sys.argv[5]
    while checkAlias(cloudfrontID, alias) != True:
        print("Checking...")
    updateRecord(hostedzoneID, old_domain, new_domain, alias)
    print("Record Updated!")

if __name__ == "__main__":
    main()