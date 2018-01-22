import boto3
import botocore
import urllib2
import json


# This method is suitable for IAM role.
def getTemporaryCertificate(service, region='us-east-1'):
    IAMSecurityUrl = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/'
    
    response = urllib2.urlopen(IAMSecurityUrl)
    response = urllib2.urlopen(IAMSecurityUrl + response.read())
    IAMTemporaryCertificate = json.loads(response.read())

    awsAK = IAMTemporaryCertificate['AccessKeyId']
    awsSK = IAMTemporaryCertificate['SecretAccessKey']
    awsToken = IAMTemporaryCertificate['Token']

    client = boto3.client(
        service,
        aws_access_key_id = awsAK,
        aws_secret_access_key = awsSK,
        region_name = region,
        aws_session_token = awsToken
    )
    
    return client

# This method is suitable for successful configuration.
def getProfileCertificate(service, profile='default'):
    session = boto3.Session(profile_name = profile)
    client = session.client(service)
    
    return client

# This method is suitable for any other situation.
def getDefaultCertificate(service):
    client = boto3.client(service)
    
    return client

# Get Client.
# Input:    String client type 'profile'|'temporary'
# Output:   Null.
def getClient(service, clientType='profile', profile='default'):
    if clientType == 'profile':
        try:
            client = getProfileCertificate(service, profile)
        except:
            client = getDefaultCertificate(service)
    elif clientType == 'temporary':
        try:
            client = getTemporaryCertificate(service)
        except:
            client = getDefaultCertificate(service)
    else:
        return None

    return client
