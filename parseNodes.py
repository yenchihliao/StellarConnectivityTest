import requests
import json
from time import sleep
from Quorum import SCPQuorum
import Utils
import matplotlib.pyplot as plt
import numpy as np


# r = requests.get("https://api.stellarbeat.io/v1/network/stellar-public")
# nodes = r.json().get("nodes")
f = open('stellar-public', 'r')
r = json.load(f)
nodes = r.get("nodes")
hash2ID = {}
def quorumParser(rawSlices):
    slices = set()
    for inner in rawSlices['innerQuorumSets']:
        slices.add(quorumParser(inner))
    for validator in rawSlices['validators']:
        slices.add(hash2ID[validator])
    threshold = rawSlices['threshold']
    return SCPQuorum(slices, threshold)
def trustedSet(rawSlices):
    ret = set()
    for inner in rawSlices['innerQuorumSets']:
        ret = ret.union(trustedSet(inner))
    for validator in rawSlices['validators']:
        ret.add(validator)
    return ret
nodeCount = len(nodes)
# trim nodes that are neither trusting others nor trusted by any
JS_MAX_NUM = 9007199254740991
notTrusting = set() # map node hash to bool
trusted = set() # node hashes that are trusted
for node in nodes:
    if(node['quorumSet']['threshold'] == JS_MAX_NUM):
        notTrusting.add(node['publicKey'])
    else:
        trusted = trusted.union(trustedSet(node['quorumSet']))
removing = notTrusting.difference(trusted)
# Assign int nodeID to every existed nodes
count = 0
for node in nodes:
    if(node['publicKey'] in removing):
        continue
    hash2ID[node['publicKey']] = count
    count += 1
# make instances of SCPQuroum
quorums = []
names = []
for node in nodes:
    if(node['publicKey'] in removing):
        continue
    if(node.get('name')):
        names.append(node['name'])
    else:
        names.append(node.get('publicKey')[:4])
    # quorum.show(True)
    quorums.append(quorumParser(node['quorumSet']))

# Evaluate the system
PR = Utils.PageRank(Utils._toMatrix(quorums), len(quorums), xAxis = names, draw = False)
NR = Utils.NodeRank(quorums, len(quorums), xAxis = names, draw = False)

class Pair():
    def __init__(self, name, rank):
        self.mName = name
        self.mRank = rank
# Output the graph with sorted rank
pairs = []
for i in range(len(quorums)):
    pairs.append((names[i], PR[i], NR[i]))
pairs.sort(key=lambda tup: tup[2], reverse=True)
for i in range(len(quorums)):
    names[i] = pairs[i][0]
    PR[i] = pairs[i][1]
    NR[i] = pairs[i][2]
l1, = plt.plot(names, PR, '*', linestyle='solid', label='PageRank')
l2, = plt.plot(names, NR, '*', linestyle='solid', label='NodeRank')
plt.legend(handles = [l1, l2])
plt.xticks(rotation='vertical')
plt.show()
