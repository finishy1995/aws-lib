import boto3
import botocore
from tools import *


SERVICE = 's3'
client = Client.getClient(SERVICE)

# Reset Client.
# Input:    String client type.
# Output:   Bool True/False.
def resetClient(clientType):
    response = Client.getClient(SERVICE, clientType)
    global client
    
    if response != None:
        client = response
        return True
    else:
        return False

# Create S3 Bucket (Will add random suffix if bucket name already exist. Max atempt 20.)
# Input:    String name. String region. String acl 'private'|'public-read'|'public-read-write'|'authenticated-read'.
# Output:   String bucket name.
def createBucket(name, region, acl='private'):
    location = getLocationByRegion(region)
    suffix = ''
    
    for i in xrange(20):
        try:
            client.create_bucket(
                ACL = acl,
                Bucket = name + suffix,
                CreateBucketConfiguration = {
                    'LocationConstraint': location
                }
            )
        except botocore.exceptions.ClientError:
            suffix = '-' + String.createRandomString(14)
            continue
        else:
            return name + suffix

# Put S3 Bucket As Website.
# Input:    String bucket name. Dir configuration, see http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.put_bucket_website.
# Output:   Void. (Status success by default)
def putBucketWebsite(bucketName, configuration={}):
    # Default configuration
    # Index:    index.html
    # Error:    error.html
    if configuration == {}:
        configuration = {
            'ErrorDocument': {
                'Key': 'error.html'
            },
            'IndexDocument': {
                'Suffix': 'index.html'
            }
        }
    
    client.put_bucket_website(
        Bucket = bucketName,
        WebsiteConfiguration = configuration
    )

# Upload Local File To S3 Bucket.
# Input:    String source path. String target path. String bucket name. String acl 'private'|'public-read'|'public-read-write'|'authenticated-read'.
# Output:   Upload response. More details: http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.put_object.
def putObject(sourcePath, targetPath, bucketName, acl='private'):
    fp = file(sourcePath, 'r')
    contentType = 'binary/octet-stream'
    # Transfer html file as text/html type.
    if (sourcePath[-5:] == '.html'):
        contentType = 'text/html'
    
    response = client.put_object(
        ACL = acl,
        Body = fp,
        Bucket = bucketName,
        Key = targetPath,
        ContentType = contentType
    )
    
    return response

# Update Object Acl.
# Input:    String file path. String bucket name. String acl 'private'|'public-read'|'public-read-write'|'authenticated-read'.
# Output:   Void.
def putObjectACL(filePath, bucketName, acl='private'):
    client.put_object_acl(
        ACL = acl,
        Bucket = bucketName,
        Key = filePath
    )

# Make S3 Bucket File Public.
# Input:    String file path. String bucket name.
# Output:   Void.
def putObjectPublic(filePath, bucketName):
    putObjectACL(filePath, bucketName, 'public-read')

# Upload all files in local folder.
# Input:    String folder path. String bucket name. String acl 'private'|'public-read'|'public-read-write'|'authenticated-read'.
# Output:   Void.
def putObjectsByFolder(folderPath, bucketName, acl='private'):
    pathsData = Path.getFilePathFrom(folderPath)
    
    for item in pathsData:
        putObject(item, item[len(folderPath):], bucketName, acl)

# Download object.
# Input:    String object key. String target path. String bucket name.
# Output:   Void.
def downloadObject(objectKey, targetPath, bucketName):
    client.download_file(bucketName, objectKey, targetPath)

# List All Buckets.
# Input:    Null.
# Output:   
def listBuckets():
    response = client.list_buckets()
    buckets = []
    
    for item in response['Buckets']:
        buckets.append(item['Name'])
    
    return buckets
