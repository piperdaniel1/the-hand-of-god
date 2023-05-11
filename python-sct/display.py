import os

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

def red(text):
    return f'\033[31m{text}\033[0m'

def green(text):
    return f'\033[32m{text}\033[0m'

def blue(text):
    return f'\033[34m{text}\033[0m'

def yellow(text):
    return f'\033[33m{text}\033[0m'

def aqua(text):
    return f'\033[36m{text}\033[0m'

def purple(text):
    return f'\033[35m{text}\033[0m'

def white(text):
    return f'\033[37m{text}\033[0m'

def black(text):
    return f'\033[30m{text}\033[0m'

def hred(text):
    return f'\033[41m{text}\033[0m'

def hgreen(text):
    return f'\033[42m{text}\033[0m'

def hblue(text):
    return f'\033[44m{text}\033[0m'

def hyellow(text):
    return f'\033[43m{text}\033[0m'

def haqua(text):
    return f'\033[46m{text}\033[0m'

def hpurple(text):
    return f'\033[45m{text}\033[0m'

def hwhite(text):
    return f'\033[47m{text}\033[0m'

def hblack(text):
    return f'\033[40m{text}\033[0m'

def light_green(text):
    return f'\033[92m{text}\033[0m'

def hlight_green(text):
    return f'\033[102m{text}\033[0m'