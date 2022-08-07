from datetime import datetime
import bot.constants as const


class Console:
    COLORS = const.COLORS

    def __init__(self) -> None:
        print(self.get_timestamp(), ' -> ',
              self.COLORS['green'], 'Started', self.COLORS['reset'], sep='')

    def get_timestamp(self) -> str:
        dateObj = datetime.now()
        last = '' if dateObj.second//10 else ' '
        return f'{dateObj.year}/{dateObj.month}/{dateObj.day} :: {dateObj.hour}:{dateObj.minute}:{dateObj.second}{last}'

    def exit_console(self, ex_type='normal'):

        print(self.get_timestamp(), ' -> ',
              self.COLORS['yellow'], '<EXIT>', self.COLORS['reset'], end='', sep='')

        if ex_type == 'normal':
            print(' normal exit')
        if ex_type == 'forced':
            print(self.COLORS['red'], 'forced exit', self.COLORS['reset'])
        exit()

    def error(self, err: str, exitN=False):
        print(self.get_timestamp(), ' -> ',
              self.COLORS['red'], '<ERROR> ', self.COLORS['reset'], err, sep='')
        if exitN:
            self.exit_console(ex_type='forced')

    def print(self, string: str):
        print(self.get_timestamp(), '->', string)
