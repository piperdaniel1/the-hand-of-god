import mss
import win32api, win32con
import winsound
import time
import sys
from display import Display

def left_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def is_alt_clicked():
    return win32api.GetAsyncKeyState(win32con.VK_MENU) < 0

def is_mouse_clicked():
    return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0

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

def get_ind(x, y, width):
    return (x + y * width) * 4

class TriggerBot:
    def __init__(self, offset=0, mode='performance'):
        self.offset = offset
        self.mode = mode
        self.MONITOR_WIDTH = 2560
        self.MONITOR_HEIGHT = 1440
        self.UPPER_OFFSET = 3
        self.SECOND_MONITOR_OFFSET = 1920
    
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
        HEIGHT = 10
        ENABLED = False
        CLICKED = False

        display = Display()
        display.is_active = ENABLED
        display.rerender()

        with mss.mss() as sct:
            while True:
                # Part of the screen to capture
                monitor = {"top": self.MONITOR_HEIGHT // 2 - HEIGHT, "left": self.MONITOR_WIDTH // 2 - WIDTH // 2 + self.SECOND_MONITOR_OFFSET, "width": WIDTH, "height": HEIGHT}

                # Grab the data
                sct_img = sct.grab(monitor)

                # Display the picture
                left_trigger = False
                right_trigger = False

                lower_mid = get_ind(WIDTH // 2, HEIGHT-1, WIDTH)

                r = sct_img.raw[lower_mid + 0] 
                g = sct_img.raw[lower_mid + 1]
                b = sct_img.raw[lower_mid + 2]

                '''
                 - Mode 1: Low Reflex Mode
                '''

                # make sure crosshair is there
                if not is_mouse_clicked():
                    if ((r < 55 and g < 55 and b > 180 ) or (r < 65 and g < 65 and b > 200)):
                        for i in range(0, len(sct_img.raw), 4):
                            r = sct_img.raw[i]
                            g = sct_img.raw[i+1]
                            b = sct_img.raw[i+2]
                            if is_trigger(r, g, b):
                                y = i // (WIDTH * 4)
                                x = (i - y * WIDTH * 4) // 4

                                if x < WIDTH // 2:
                                    left_trigger = True
                                else:
                                    right_trigger = True
                    
                        if left_trigger and right_trigger and ENABLED:
                            left_click()
                            mss.tools.to_png(sct_img.rgb, sct_img.size, output="last-fire.png")
                            time.sleep(0.2)
                    else:
                        if is_alt_clicked():
                            if not CLICKED:
                                if ENABLED:
                                    winsound.Beep(1000, 100)
                                    display.is_active = False
                                else:
                                    winsound.Beep(2000, 100)
                                    display.is_active = True

                                display.rerender()
                                ENABLED = not ENABLED
                                
                            CLICKED = True
                        else:
                            CLICKED = False
                    # elif r == 255 and g == 255 and b == 0:
                    #     for i in range(0, len(sct_img.raw), 4):
                    #         r = sct_img.raw[i]
                    #         g = sct_img.raw[i+1]
                    #         b = sct_img.raw[i+2]
                    #         if is_trigger(r, g, b):
                    #             y = i // (WIDTH * 4)
                    #             x = (i - y * WIDTH * 4) // 4

                    #             if x < WIDTH // 2:
                    #                 left_trigger = True
                    #             else:
                    #                 right_trigger = True
                    
                    #     if left_trigger and right_trigger and ENABLED:
                    #         left_click()
                    #         mss.tools.to_png(sct_img.rgb, sct_img.size, output="last-fire.png")
                    #         time.sleep(0.15)



    # Used for testing colors
    def _run_test(self):
        while True:
            with mss.mss() as sct:
                # Part of the screen to capture
                monitor = {"top": 0, "left": self.SECOND_MONITOR_OFFSET, "width": self.MONITOR_WIDTH, "height": self.MONITOR_HEIGHT}

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