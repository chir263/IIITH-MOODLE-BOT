from bot.moodle import Moodle
from bot.console import Console
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
import sys

global_list = []


def my_moodle(mood: Moodle, courses: list):

    if len(courses) == 1:
        mood.open_course(courses[0], new_win=True)
    elif len(courses):
        mood.open_course(courses[0], new_win=True)
        for i in range(1, len(courses)):

            if courses[i] == 'grd':
                mood.check_inst(courses=courses, i=i)
                mood.grade(mood.current_course)

            elif courses[i].startswith('ins'):
                inst = courses[i].split('=')
                mood.check_inst(courses=courses, i=i)
                mood.get_instance(mood.current_course, inst=inst)

            else:
                mood.open_course(courses[i], new_win=True)


def startMoodle(courses: list):
    console = Console()
    try:
        with Moodle(console=console) as mood:
            global global_list
            mood.land_first_page()
            mood.login()
            global_list = courses
            my_moodle(mood, courses)
            while True:
                string = input('>> ').strip()
                if string == 'q':
                    mood.console.exit_console()
                elif string == '':
                    continue
                else:
                    string = string.split(' ')
                    next_list = [x.strip() for x in string]
                    global_list = next_list
                    my_moodle(mood, next_list)

    except NoSuchWindowException:
        startMoodle(global_list)
    except WebDriverException:
        startMoodle(global_list)
    except Exception as err:
        console.error(type(err).__name__, exitN=True)


if __name__ == '__main__':
    sys.stdout.write('\33]0;Moodle\a')
    sys.stdout.flush()
    courses = []
    i = 1
    while i < len(sys.argv):
        courses.append(sys.argv[i])
        i += 1
    startMoodle(courses)
