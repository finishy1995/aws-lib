import boto3
import botocore
from tools import *


SERVICE = 'dynamodb'
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
        
# Batch get items.
# Input:    String table. Array data all actions.
# Output:   Response.
def batchGetItemsByArray(table, data):
    response = client.batch_get_item(
        RequestItems = {
            table: {
                'Keys': data
            }
        }
    )
    
    return response['Responses'][table]

# Batch write items.
# Input:    String table. Array data all actions.
# Output:   Dir. Failure actions. 
def batchWriteItemsByArray(table, data):
    response = client.batch_write_item(
        RequestItems = {
            table: data
        }
    )
    
    return response['UnprocessedItems']

# Get DDB Item.
# Input:    String table. Array data all actions. String expression.
# Output:   Dir item details. 
def getItemByArray(table, data, expression=''):
    if expression == '':
        response = client.get_item(
            TableName = table,
            Key = data
        )
    else:
        response = client.get_item(
            TableName = table,
            Key = data,
            ProjectionExpression = expression
        )
    
    if response.has_key('Item'):
        return response['Item']
    else:
        return {}

# Query DDB.
# Input:    String table. String key. Valid value. Int limit. String expression.
# Output:   Query response.
def query(table, key, value, valueType='S', limit=100, expression=''):
    items = []
    flag = True
    if limit == -1:
        queryLimit = 100
    else:
        queryLimit = limit
    
    if expression == '':
        while (flag):
            response = client.query(
                TableName = table,
                Limit = queryLimit,
                KeyConditionExpression = "%s = :value" % (key),
                ExpressionAttributeValues = {
                    ':value': String.createJsonFormat(valueType, str(value))
                }
            )
            
            if limit != -1:
                queryLimit -= response['Count']
                if queryLimit == 0:
                    items = items + response['Items']
                    break
                elif queryLimit < 0:
                    for item in xrange(response['Count'] + queryLimit):
                        items.append(item)
                    break
                    
            items = items + response['Items']
            flag = response.has_key('LastEvaluatedKey')
    else:
        while (flag):
            response = client.query(
                TableName = table,
                Limit = queryLimit,
                KeyConditionExpression = "%s = :value" % (key),
                ExpressionAttributeValues = {
                    ':value': String.createJsonFormat(valueType, str(value))
                },
                ProjectionExpression = expression
            )
            
            if limit != -1:
                queryLimit -= response['Count']
                if queryLimit == 0:
                    items = items + response['Items']
                    break
                elif queryLimit < 0:
                    for item in xrange(response['Count'] + queryLimit):
                        items.append(item)
                    break
                    
            items = items + response['Items']
            flag = response.has_key('LastEvaluatedKey')
            