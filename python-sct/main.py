import mss
import win32api, win32con
import time

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def is_trigger(r, g, b):
    TRIGGER_PIXEL = (210, 170, 210)
    tolerance = 60

    if abs(r - TRIGGER_PIXEL[0]) < tolerance and abs(g - TRIGGER_PIXEL[1]) < tolerance and abs(b - TRIGGER_PIXEL[2]) < tolerance:
        return True
    
    return False


WIDTH = 200
while True:
    with mss.mss() as sct:
        # Part of the screen to capture
        monitor = {"top": 537, "left": 960 - WIDTH // 2, "width": WIDTH, "height": 1}

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        # mss.tools.to_png(sct_img.rgb, sct_img.size, output="monitor-1.png")

        # Display the picture
        left_trigger = False
        right_trigger = False

        r = sct_img.raw[WIDTH // 2 * 4]
        g = sct_img.raw[WIDTH // 2 * 4 + 1]
        b = sct_img.raw[WIDTH // 2 * 4 + 2]

        # make sure crosshair is there
        if (r < 55 and g < 55 and b > 180 ) or (r < 65 and g < 65 and b > 200):
            for i in range(0, len(sct_img.raw)//2, 4):
                r = sct_img.raw[i]
                g = sct_img.raw[i+1]
                b = sct_img.raw[i+2]
                if is_trigger(r, g, b):
                    left_trigger = True
                    break

            for i in range(len(sct_img.raw)//2, len(sct_img.raw), 4):
                r = sct_img.raw[i]
                g = sct_img.raw[i+1]
                b = sct_img.raw[i+2]
                if is_trigger(r, g, b):
                    right_trigger = True
                    break
        
            if left_trigger and right_trigger:
                left_click()
                time.sleep(0.2)