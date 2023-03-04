import mss
import win32api, win32con
import time
import sys

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def is_trigger(r, g, b):
    # Standard trigger pixel
    TRIGGER_PIXEL = (255, 110, 255)
    tolerance_r = 20
    tolerance_g = 50
    tolerance_b = 20

    if abs(r - TRIGGER_PIXEL[0]) < tolerance_r and abs(g - TRIGGER_PIXEL[1]) < tolerance_g and abs(b - TRIGGER_PIXEL[2]) < tolerance_b:
        return True

    # A sort of dark trigger pixel
    TRIGGER_PIXEL = (239, 116, 218)
    tolerance_r = 20
    tolerance_g = 20
    tolerance_b = 20
    
    if abs(r - TRIGGER_PIXEL[0]) < tolerance_r and abs(g - TRIGGER_PIXEL[1]) < tolerance_g and abs(b - TRIGGER_PIXEL[2]) < tolerance_b:
        return True

    # A bit darker trigger pixel
    TRIGGER_PIXEL = (177, 57, 156)
    tolerance_r = 20
    tolerance_g = 20
    tolerance_b = 20
    
    if abs(r - TRIGGER_PIXEL[0]) < tolerance_r and abs(g - TRIGGER_PIXEL[1]) < tolerance_g and abs(b - TRIGGER_PIXEL[2]) < tolerance_b:
        return True
    
    # A bit lighter trigger pixel
    TRIGGER_PIXEL = (245, 182, 245)
    # Keep tolerances low to avoid picking up white
    tolerance_r = 20
    tolerance_g = 30
    tolerance_b = 20
    
    if abs(r - TRIGGER_PIXEL[0]) < tolerance_r and abs(g - TRIGGER_PIXEL[1]) < tolerance_g and abs(b - TRIGGER_PIXEL[2]) < tolerance_b:
        return True

    return False

class TriggerBot:
    def __init__(self, offset=0, mode='performance'):
        self.offset = offset
        self.mode = mode
    
    def run(self):
        if self.mode == 'performance':
            print("Starting trigger bot in performance mode")
            self._run_perf()
        elif self.mode == 'test':
            print("Starting trigger bot in test mode")
            self._run_test()
        else:
            raise Exception('Invalid mode')
    
    def _run_perf(self):
        WIDTH = 100
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
                        time.sleep(1.5)

    # Used for testing colors
    def _run_test(self):
        while True:
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}

                # Grab the data
                sct_img = sct.grab(monitor)

                # Change any trigger pixels to a red tint
                for i in range(0, len(sct_img.raw), 4):
                    r = sct_img.raw[i]
                    g = sct_img.raw[i+1]
                    b = sct_img.raw[i+2]
                    if is_trigger(r, g, b):
                        sct_img.raw[i] = 0
                        sct_img.raw[i+1] = 0
                        sct_img.raw[i+2] = min(255, b + 15)

                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output="monitor-1.png", level=0)

                # # Display the picture
                # left_trigger = False
                # right_trigger = False

                # r = sct_img.raw[WIDTH // 2 * 4]
                # g = sct_img.raw[WIDTH // 2 * 4 + 1]
                # b = sct_img.raw[WIDTH // 2 * 4 + 2]

                # # make sure crosshair is there
                # if (r < 55 and g < 55 and b > 180 ) or (r < 65 and g < 65 and b > 200):
                #     for i in range(0, len(sct_img.raw)//2, 4):
                #         r = sct_img.raw[i]
                #         g = sct_img.raw[i+1]
                #         b = sct_img.raw[i+2]
                #         if is_trigger(r, g, b):
                #             left_trigger = True
                #             break

                #     for i in range(len(sct_img.raw)//2, len(sct_img.raw), 4):
                #         r = sct_img.raw[i]
                #         g = sct_img.raw[i+1]
                #         b = sct_img.raw[i+2]
                #         if is_trigger(r, g, b):
                #             right_trigger = True
                #             break
                
                #     if left_trigger and right_trigger:
                #         left_click()
                #         time.sleep(0.2)

def main():
    if len(sys.argv) == 1:
        mode = 'performance'
        offset = 0
    elif len(sys.argv) == 2:
        mode = sys.argv[1]
        offset = 0
    elif len(sys.argv) == 3:
        mode = sys.argv[1]
        offset = int(sys.argv[2])
    else:
        raise Exception('Invalid arguments')
    
    bot = TriggerBot(offset=offset, mode=mode)
    bot.run()

main()