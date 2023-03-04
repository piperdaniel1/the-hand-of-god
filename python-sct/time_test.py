import mss
import time
import numpy as np
from matplotlib import pyplot as plt
import win32api, win32con

def ns_to_ms(ns):
    return ns / 1000000

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 800, "height": 600}

    # Grab the data
    data = []
    for _ in range(1000):
        start = time.perf_counter_ns()
        sct_img = sct.grab(monitor)
        end = time.perf_counter_ns()

        print(ns_to_ms(end - start))
        data.append(ns_to_ms(end - start))

    
data = np.array(data)

# Convert all MS nums to FPS
fps = 1000 / data

# Calculate the mean and variance
mean = np.mean(fps)
var = np.var(fps)

print("The average FPS is: {}".format(mean))
plt.plot(fps)
plt.axhline(mean, color='r')
plt.axhline(mean + var, color='g')
plt.axhline(mean - var, color='g')
plt.show()

# Save to the picture file
# mss.tools.to_png(sct_img.rgb, sct_img.size, output="monitor-1.png")

# Display the picture
# mss.tools.to_png(sct_img.rgb, sct_img.size)