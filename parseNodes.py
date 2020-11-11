import requests
import json
from time import sleep
from Quorum import SCPQuorum
import Utils

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
Quorums = []
for node in nodes:
    if(node['publicKey'] in removing):
        continue
    quorum = quorumParser(node['quorumSet'])
    # quorum.show(True)
    Quorums.append(quorum)

# Evaluate the system
# Utils.NodeRank(Quorums, len(Quorums))
