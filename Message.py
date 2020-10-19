class SCPMessage():
    """
    mSender(int): Node ID
    mHeight(int): The height of the message
    mView(int): The view of the message.
    mVote(auto): The consensus target
    mSlices(auto): The slices setting of the sender
    """
    def __init__(self, snder, height, view, vote, slices):
        self.mSender = snder
        self.mHeight = height
        self.mView = view
        self.mVote = vote
        self.mSlices = slices
    def show(self):
        print('Message: sender{} @ view {} -- {}'.format(self.mSender, self.mView, self.mVote))
