import random
import string


# Create Random String.
# Input:    String length.
# Output:   String random string.
def createRandomString(length):
    letters = string.ascii_lowercase
    
    return ''.join(random.choice(letters) for i in range(length))
    
# Get Location Name By Region ID.
# Input:    String region.
# Output:   String location.
def getLocationByRegion(region):
    location = region
    if region == 'us-east-1':
        location = ''
        
    return location

# Json Format.
# Input:    String Type. String value.
# Output:   Format Dir.
def createJsonFormat(valueType, value):
    return { valueType: value }

# Number Json Format.
# Input:    Int value.
# Output:   Format Dir.
def createNumberFormat(value):
    return createJsonFormat('N', str(value))
    
# String Json Format.
# Input:    String value.
# Output:   Format Dir.
def createStringFormat(value):
    return createJsonFormat('S', value)
