import Node

def decision():
    data = [[]]
    f = open('Outside.csv')
    for line in f:
        line = line.strip("\r\n")
        data.append(line.split(','))
    data.remove([])
    tree = {'outlook': {'rainy': {'temperature': {'mild': {'humidity': {'high': {'windy': {'TRUE': 'no', 'FALSE': 'yes'}}, 'normal': 'yes'}}, 'cool': {'humidity': {'normal': {'windy': {'TRUE': 'no', 'FALSE': 'yes'}}}}}}, 'overcast': {'temperature': {'hot': 'no', 'mild': 'yes', 'cool': 'no'}}, 'sunny': {'temperature': {'hot': {'humidity': {'high': {'windy': {'TRUE': 'no', 'FALSE': 'yes'}}}}, 'mild': 'no', 'cool': 'yes'}}}}
    attributes = ['outlook', 'temperature', 'humidity', 'windy', 'all nighter', 'lot of homework', 'lazy', 'medical issues', 'grade', 'outside']
    count = 0
    list = {}
    dc = 1
    for entry in data:
        count += 1
        tempDict = tree.copy()
        result = ""
        while(isinstance(tempDict, dict)):
            root = Node.Node(tempDict.keys()[0], tempDict[tempDict.keys()[0]])
            tempDict = tempDict[tempDict.keys()[0]]
            index = attributes.index(root.value)
            value = entry[index]
            if(value in tempDict.keys()):
                child = Node.Node(value, tempDict[value])
                result = tempDict[value]
                tempDict = tempDict[value]
            else:
                #list.append( "can't process input %s" % count)
                result = "?"
                
                break
        list[dc] = "entry%s = %s" % (count, result)
        dc+=1

    return list
