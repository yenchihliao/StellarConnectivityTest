import numpy as np
import matplotlib.pyplot as plt

x = np.arange(27)
x *= 6
x += 4
yo = [2173, 3338, 3708, 4018, 4088, 4184, 4141, 4296, 4351, 4429, 4594, 4511, 4609, 4552, 4588, 4532, 5194, 5083, 4953, 4916, 5022, 4924, 4876, 4848, 4778, 4932, 4850]
yc = [8324, 15294, 19364, 21914, 24622, 26455, 28309, 29841, 31311, 32344, 33715, 34908, 35684, 36367, 37618, 38111, 40035, 41394, 41697, 41699, 43008, 44221, 44187, 44325, 44926, 45678, 46477]
plt.plot(x, yo, c='y', marker='o')
plt.plot(x, yc, c='y', marker='D')


x40n = np.arange(4)
x40n += 1
x40n *= 40
yo40n = [9575, 13451, 16623, 19661]
yc40n = [33058, 45791, 55164, 63478]
plt.plot(x40n, yo40n, c='b', marker='o')
plt.plot(x40n, yc40n, c='b', marker='D')

x20n = np.arange(8)
x20n += 1
x20n *= 20
yo20n = [12562, 17597, 24786, 29191, 37210, 42278, 48666, 57828]
yc20n = [27550, 39116, 50969, 59046, 68294, 75516, 81894, 91999]
plt.plot(x20n, yo20n, c='g', marker='o')
plt.plot(x20n, yc20n, c='g', marker='D')

x8n = np.arange(8)
x8n += 1
x8n *= 8
yo8n = [21793, 33450, 63363, 80728, 100512, 153675, 186251, 223118]
yc8n = [23204, 36271, 53390, 64509, 74777, 93034, 103363, 115640]
plt.plot(x8n, yo8n, c='r', marker='o')
plt.plot(x8n, yc8n, c='r', marker='D')


x6n = np.arange(5)
x6n += 1
x6n *= 6
yo6n = [39109, 66844, 103219, 149879, 215784]
yc6n = [28673, 45598, 63103, 80437, 99405]
plt.plot(x6n, yo6n, c='c', marker='o')
plt.plot(x6n, yc6n, c='c', marker='D')


x5n = np.arange(5)
x5n += 1
x5n *= 5
yo5n = [34059, 55180, 156786, 203143, 263998]
yc5n = [25535, 40041, 79703, 91040, 105913]
plt.plot(x5n, yo5n, c='m', marker='o')
plt.plot(x5n, yc5n, c='m', marker='D')

x4n = np.arange(5)
x4n += 1
x4n *= 4
yo4n = [27360, 110523, 334202, 303413, 720450]
yc4n = [21080, 66285, 158484, 120103, 215210]
plt.plot(x4n, yo4n, c='y', marker='o')
plt.plot(x4n, yc4n, c='y', marker='D')

plt.plot([], [], c='b', label='f=40')
plt.plot([], [], c='g', label='f=20')
plt.plot([], [], c='r', label='f=8')
plt.plot([], [], c='c', label='f=6')
plt.plot([], [], c='m', label='f=5')
plt.plot([], [], c='y', label='f=4')
plt.plot([], [], c='black', marker='o', label='vFBAS')
plt.plot([], [], c='black', marker='D', label='SCP')
plt.legend(loc='upper right')
plt.xlabel('Total node count')
plt.ylabel('Average timeout')
plt.show()
