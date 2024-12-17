import sys
import os
from datetime import datetime

from rich.console import Console
from rich.padding import Padding
from rich.text import Text


class Logger:
    def __init__(self, log_file='logfile.log'):
        self.log_type = 'Information'
        self.date_time = 'Unknown'
        self.website = 'Unknown'
        self.username = 'Anonymous'
        self.module = 'Unknown'
        self.message = 'No message provided'

        self.__hide_cursor()
        self.console = Console()

        project_dir = os.path.dirname(os.path.abspath(__file__))
        main_project_dir = os.path.abspath(os.path.join(project_dir, os.pardir))
        self.log_file = os.path.join(main_project_dir, log_file)

    @staticmethod
    def __hide_cursor():
        """Hides the cursor in the terminal."""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def __get_renderable_log(self):
        self.console.print('')

        self.date_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        renderable = f'[red dim] ╭─[ [/red dim][red]{self.date_time}[/red][red dim] ]──([/red dim] [red]{self.website} ~[/red] [purple]{self.username}[/purple] [red dim])'

        self.console.print(Padding(renderable, (-1)))
        self.console.print(Text(f' │ ', style='red dim'))
        self.console.print(Text(f' ╰───', style='red dim'), end='')
        self.console.print(Text(f'( {self.module} ) ~ ', style='red'), end='')
        self.console.print(Text(f'{self.message}', style='grey78', overflow='ignore', no_wrap=True), end='')

    def __write_to_log_file(self):
        formatted_log = f'[ {self.date_time} ]-[{self.log_type}]-[ {self.website}@{self.username} ]-( {self.module} ) ~# {self.message}'

        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                file.write(formatted_log + '\n')
        except Exception as e:
            print(f'Failed to write to log file: {e}', file=sys.stderr)

    def update(self, log_type=None, website=None, username=None, module=None, message=None):
        if log_type:
            self.log_type = log_type
        if website:
            self.website = website
        if username:
            self.username = username
        if module:
            self.module = module
        if message:
            self.message = message

        os.system('cls' if os.name == 'nt' else 'clear')

        self.__get_renderable_log()

        self.__write_to_log_file()
