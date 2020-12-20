import sys
import math
import oneShot_adaptive, combine_adaptive

if __name__ == '__main__':
    targetHeight = 10000
    maxNode = 85
    faultyRate = int(sys.argv[1])
    if(faultyRate == 0):
        gap = 1
    else:
        gap = math.ceil(math.ceil(100/faultyRate) / 3)
    minNode = gap
    maxNode = max(85, gap*5)
    rets = []
    rets.append(oneShot_adaptive.runUtilHeight(targetHeight, minNode, maxNode, gap, faultyRate))
    print('oneShot faulty rate of {} with {} gap yeild:'.format(faultyRate, gap))
    print(rets)

    rets = []
    rets.append(combine_adaptive.runUtilHeight(targetHeight, minNode, maxNode, gap, faultyRate))
    print('combine faulty rate of {} with {} gap yeild:'.format(faultyRate, gap))
    print(rets)
