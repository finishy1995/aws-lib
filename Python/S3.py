import boto3
import botocore
import random
import string
import commands
import Client


client = Client.getProfileCertificate('s3')

# Create Random String.
# Input:    String length.
# Output:   String random string.
def createRandomString(length):
    letters = string.ascii_lowercase
    
    return ''.join(random.choice(letters) for i in range(length))
    
# Get All File Path From Folder Path.
# Input:    String folder path.
# Output:   Array folders file data [filePath, ...].
def getFilePathFrom(folderPath):
    if folderPath[-1] != '/':
        folderPath += '/'
    fileData = []
    
    (status, output) = commands.getstatusoutput('ls ' + folderPath)
    if status == 0:
        files = output.split('\n')
    else:
        files = []
    
    for item in files:
        if item.find('.') != -1:
            fileData.append(folderPath + item)
        else:
            fileData += getFilePathFrom(folderPath + item + '/')
    
    return fileData
    
# Get Location Name By Region ID.
# Input:    String region.
# Output:   String location.
def getLocationByRegion(region):
    location = region
    if region == 'us-east-1':
        location = ''
        
    return location

# Set Client Type.
# Input:    String client type 'profile'|'temporary'
# Output:   Null.
def setClientType(clientType):
    global client
    
    if clientType == 'profile':
        client = Client.getProfileCertificate('s3')
    elif clientType == 'temporary':
        client = Client.getTemporaryCertificate('s3')

# ------------------------------------------------------------ #


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
            suffix = '-' + createRandomString(14)
            continue
        else:
            return name + suffix

# Put S3 Bucket As Website.
# Input:    String bucket name. Dir configuration, see http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.put_bucket_website.
# Output:   Void. (Status success by default)
def putBucketWebsite(bucketName, configuration={}):
    client = boto3.client('s3')
    
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
    client = boto3.client('s3')
    
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
    client = boto3.client('s3')
    
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
    if folderPath[-1] != '/':
        folderPath += '/'
    
    pathsData = getFilePathFrom(folderPath)
    
    for item in pathsData:
        putObject(item, item[len(folderPath):], bucketName, acl)

# Download object.
# Input:    String object key. String target path. String bucket name.
# Output:   Void.
def getObject(objectKey, targetPath, bucketName):
    client = boto3.client('s3')
    
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
    