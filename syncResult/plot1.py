import numpy as np
import matplotlib.pyplot as plt

x = np.arange(27)
x *= 6
x += 4
yo = [2173, 3338, 3708, 4018, 4088, 4184, 4141, 4296, 4351, 4429, 4594, 4511, 4609, 4552, 4588, 4532, 5194, 5083, 4953, 4916, 5022, 4924, 4876, 4848, 4778, 4932, 4850]
yc = [8324, 15294, 19364, 21914, 24622, 26455, 28309, 29841, 31311, 32344, 33715, 34908, 35684, 36367, 37618, 38111, 40035, 41394, 41697, 41699, 43008, 44221, 44187, 44325, 44926, 45678, 46477]
plt.plot(x, yo, marker='o', label='vFBAS')
plt.plot(x, yc, marker='D', label='SCP')


plt.legend(loc='upper left')
plt.xlabel('Total node count')
plt.ylabel('Timeout per 10000 height')
plt.show()
