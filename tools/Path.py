import commands


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
    