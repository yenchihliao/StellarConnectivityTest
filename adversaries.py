import sys
import math
import oneShot_adaptive, combine_adaptive

if __name__ == '__main__':
    targetHeight = 10000
    maxNode = 85
    faultyRate = float(sys.argv[1])
    # set the iteration
    if(faultyRate == 0):
        iteration = 27
    elif(faultyRate == 2.5):
        iteration = 4
    elif(faultyRate == 5):
        iteration = 8
    elif(faultyRate == 10):
        iteration = 16
    elif(faultyRate == 12.5):
        iteration = 8
    elif(faultyRate > 13):
        iteration = 5
    else:
        iteration = 7

    ret1 = oneShot_adaptive.runUtilHeight(targetHeight, faultyRate, iteration)
    ret2 = combine_adaptive.runUtilHeight(targetHeight, faultyRate, iteration)

    print('faulty rate of {}:'.format(faultyRate))
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
