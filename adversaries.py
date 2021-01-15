import sys
import math
import oneShot_adaptive, combine_adaptive

if __name__ == '__main__':
    targetHeight = 10000
    maxNode = 85
    invFaultyRate = float(sys.argv[1])
    # set the iteration
    if(invFaultyRate == 0):
        iteration = 27
    elif(invFaultyRate < 8):
        iteration = 5
    elif(invFaultyRate < 11):
        iteration = 8
    else:
        iteration = math.floor(160/invFaultyRate)

    ret1 = oneShot_adaptive.runUtilHeight(targetHeight, invFaultyRate, iteration)
    ret2 = combine_adaptive.runUtilHeight(targetHeight, invFaultyRate, iteration)

    print('faulty rate of {}:'.format(invFaultyRate))
    print(ret1, ret2)
    # maxNode = max(85, gap*5)
    # rets = []
    # rets.append(oneShot_adaptive.runUtilHeight(targetHeight, minNode, maxNode, gap, faultyRate))
    # print('oneShot faulty rate of {} with {} gap yeild:'.format(faultyRate, gap))
    # print(rets)
    #
    # rets = []
    # rets.append(combine_adaptive.runUtilHeight(targetHeight, minNode, maxNode, gap, faultyRate))
    # print(rets)
