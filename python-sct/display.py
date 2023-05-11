import os
from sre_constants import SUBPATTERN
import sys
from colors import *

# display for trigger
class Display:
    def __init__(self):
        self.is_active = False
        self.disp_width = 69 # must be 4 * x + 1
        assert(self.disp_width % 4 == 1)
    
    def _center_line(self, line, fmt_funcs=[]):
        fmt_line = line
        for fmt_func in fmt_funcs:
            fmt_line = fmt_func(fmt_line)

        padding = ' ' * ((self.disp_width - len(line) - 2) // 2)
        subpadding = ' ' * (((self.disp_width - len(line) - 2) // 2) - 1)

        full_line = '|' + padding + line + padding + '|'

        if len(full_line) > self.disp_width:
            full_line = '|' + padding + fmt_line + subpadding + '|'
        elif len(full_line) < self.disp_width:
            full_line = '|' + padding + fmt_line + padding + ' ' + '|'
        else:
            full_line = '|' + padding + fmt_line + padding + '|'


        print(full_line)
    
    def _gun_art(self, fmt_funcs=[]):
        gun = r'''
                           ______                
        |\_______________ (_____\\______________ 
HH======#H###############H#######################
        ' ~""""""""""""""`##(_))#H\"""""Y########
                          ))    \#H\       `"Y###
                          "      }#H)            '''

        lines = gun.split('\n')
        max_len_line = max([len(line) for line in lines])

        assert(max_len_line < self.disp_width - 2)

        for line in lines:
            padding = ' ' * ((self.disp_width - len(line) - 2) // 2)
            subpadding = ' ' * (((self.disp_width - len(line) - 2) // 2) - 1)

            fmt_line = line
            for fmt_func in fmt_funcs:
                fmt_line = fmt_func(fmt_line)

            full_line = '|' + padding + line + padding + '|'
            if len(full_line) > self.disp_width:
                full_line = '|' + padding + fmt_line + subpadding + '|'
            elif len(full_line) < self.disp_width:
                full_line = '|' + padding + fmt_line + padding + ' ' + '|'
            else:
                full_line = '|' + padding + fmt_line + padding + '|'
            print(full_line)
    
    def _empty_line(self):
        print('|' + ' ' * (self.disp_width - 2) + '|')

    def rerender(self):
        os.system('cls')
        print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
        self._empty_line()
        self._center_line('The Hand of GOD', [aqua])
        self._gun_art([aqua] if not self.is_active else [red])
        self._empty_line()
        self._center_line('Current Status: ' + ('Active' if self.is_active else 'Inactive'), [aqua] if not self.is_active else [red])
        self._empty_line()
        print('+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+')
        pass

if __name__ == '__main__':
    display = Display()
    display.rerender()