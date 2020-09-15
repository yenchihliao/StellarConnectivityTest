class SCPMessage():
    def __init__(snder, rcver, view, vote, slices):
        self.mSender = snder
        self.mRecver = rcver
        self.mView = view
        self.mVote = vote
        self.mSlices = slices
