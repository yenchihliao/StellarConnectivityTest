class Quorum():
    def __init__(self):
        pass
    def satisfy(self, peers):
        pass
    def includes(self, v):
        pass
    def allMember(self, nodeCount):
        pass
    def toVector(self):
        pass
    def show(self):
        pass


"""
-----------
SCPQuorum
-----------
mSlices: set<SCPQuroum || nodeID>
mThreashold: int
-----------
"""
class SCPQuorum(Quorum):
    def __init__(self, slices, threshold):
        self.mSlices = slices
        self.mThreshold = threshold
    def satisfiedBy(self, peers):
        count = 0
        for s in self.mSlices:
            if(type(s) == type(self)):
                if(s.satisfiedBy(peers)):
                    count += 1
            else:
                for peer in peers:
                    if(peer == s):
                        count += 1
        return count >= self.mThreshold

    def includes(self, v):
        for s in self.mSlices:
            if(type(s) == type(self)):
                if(s.includes(v)):
                    return True
            else:
                if(s == v):
                    return True
        return False
    # INPUT: # of total nodes, nodeCount, in the System.
    # OUTPUT: Set S with all the trusted node.
    def allMember(self, nodeCount):
        vec = self.toVector(nodeCount)
        S = set()
        for i in range(nodeCount):
            if vec[i] > 0:
                S.add(i)
        return S

    # INPUT: # of total nodes, nodeCount, in the System.
    # OUTPUT: Vector v, where v[i] = # of node i appears in slice of this node.
    def toVector(self, nodeCount):
        vec = [0] * nodeCount
        for s in self.mSlices:
            if(type(s) == type(self)):
                vec2 = s.toVector(nodeCount)
                for i in range(nodeCount):
                    vec[i] += vec2[i]
            else:
                vec[int(s)] += 1
        return vec

    # INPUT: prnt decides whether to print the outcome
    # OUTPUT: visualize the slicesSet.
    def show(self, prnt = False):
        ret = ""
        ret += "{"
        for s in self.mSlices:
            if(type(s) == type(self)):
                ret += s.show()
            else:
                ret += str(s)
            ret += ", "
        try:
            ret = ret[:-2]
        except:
            pass
        ret += ("}" + str(self.mThreshold))
        if(prnt):
            print(ret)
        return ret

if __name__ == '__main__':
    q1 = SCPQuorum({1, 2, 3}, 3)
    q2 = SCPQuorum({4, 5, q1}, 2)
    q3 = SCPQuorum({6, 7, q2}, 1)
    q3.show(True)
    print(q1.includes(1), q1.includes(4), q1.includes(6))
    print(q2.includes(1), q2.includes(4), q2.includes(6))
    print(q3.includes(1), q3.includes(4), q3.includes(6))
