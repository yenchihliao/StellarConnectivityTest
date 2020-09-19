class Quorum():
    def __init__(self):
        pass

class SCPQuorum(Quorum):
    def __init__(self, slices, threshold):
        self.mSlices = slices
        self.mThreshold = threshold
