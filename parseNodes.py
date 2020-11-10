import requests
import json
from time import sleep
from Quorum import SCPQuorum

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
# Assign int nodeID to every existed nodes
for i in range(len(nodes)):
    hash2ID[nodes[i]['publicKey']] = i
# make instances of SCPQuroum
Quorums = []
for node in nodes:
    quorum = quorumParser(node['quorumSet'])
    quorum.show(True)
    Quorums.append(quorum)
