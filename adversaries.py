import sys
import math
import oneShot_adaptive, combine_adaptive

if __name__ == '__main__':
    targetHeight = 10000
    maxNode = 85
    limit = 50 # the maximum trails before finding the intersection
    faultyRate = int(sys.argv[1])
    if(faultyRate == 0):
        gap = 1
    else:
        gap = math.ceil(math.ceil(100/faultyRate) / 3)
    minNode = max(4, gap * 3)
    print('minNode = {}'.format(minNode))

    ret1 = []
    ret2 = []
    while(limit > 0):
        limit -= 1
        ret1.append(oneShot_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
        ret2.append(combine_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
        minNode += (gap * 3)
        if(ret1[-1] > ret2[-1]):
            break
    while(limit > 45):
        limit -= 1
        ret1.append(oneShot_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
        ret2.append(combine_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
        minNode += (gap * 3)
    ret1.append(oneShot_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
    ret2.append(combine_adaptive.runUtilHeight(targetHeight, minNode, minNode+1, gap, faultyRate))
    print('faulty rate of {} with {} gap yeild:'.format(faultyRate, gap))
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
