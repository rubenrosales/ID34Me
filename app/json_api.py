from flask import Flask, jsonify, request
import requests
import twitter
import json
import re
import urlparse
from app import app
import ConfigParser
import time
import DecisionTree
import id3decision

def id3():
    #Insert input file
    #file = open('train.csv')
    file = open('OutsideTraining.csv')
    target = "outside"
    data = [[]]
    for line in file:
        line = line.strip("\r\n")
        data.append(line.split(','))
    
    data.remove([])

    attributes = data[0]
    data.remove(attributes)
    #Run ID3
    tree = DecisionTree.makeTree(data, attributes, target, 0)
    print tree
    print "generated decision tree"
    #Generate program
    file = open('program.py', 'w')
    file.write("import Node\n\n")
    #open input file
    file.write("data = [[]]\n")
    """
        IMPORTANT: Change this file path to change testing data
        """
    file.write("f = open('Outside.csv')\n")
    #gather data
    file.write("for line in f:\n\tline = line.strip(\"\\r\\n\")\n\tdata.append(line.split(','))\n")
    file.write("data.remove([])\n")
    #input dictionary tree
    file.write("tree = %s\n" % str(tree))
    file.write("attributes = %s\n" % str(attributes))
    file.write("count = 0\n")
    file.write("for entry in data:\n")
    file.write("\tcount += 1\n")
    #copy dictionary
    file.write("\ttempDict = tree.copy()\n")
    file.write("\tresult = \"\"\n")
    #generate actual tree
    file.write("\twhile(isinstance(tempDict, dict)):\n")
    file.write("\t\troot = Node.Node(tempDict.keys()[0], tempDict[tempDict.keys()[0]])\n")
    file.write("\t\ttempDict = tempDict[tempDict.keys()[0]]\n")
    #this must be attribute
    file.write("\t\tindex = attributes.index(root.value)\n")
    file.write("\t\tvalue = entry[index]\n")
    #ensure that key exists
    file.write("\t\tif(value in tempDict.keys()):\n")
    file.write("\t\t\tchild = Node.Node(value, tempDict[value])\n")
    file.write("\t\t\tresult = tempDict[value]\n")
    file.write("\t\t\ttempDict = tempDict[value]\n")
    #otherwise, break
    file.write("\t\telse:\n")
    file.write("\t\t\tprint \"can't process input %s\" % count\n")
    file.write("\t\t\tresult = \"?\"\n")
    file.write("\t\t\tbreak\n")
    #print solutions
    file.write("\tprint (\"entry%s = %s\" % (count, result))\n")
    print "written program"

@app.route('/id3')
def index():
    result = id3decision.decision()
    ## dictionary to hold statuses user requested ##
    statuses = {'next_cursor': 'null', 'statuses': []}
    print result
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run()