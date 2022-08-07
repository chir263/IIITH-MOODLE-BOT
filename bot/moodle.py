from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bot.constants as const
import re


class Moodle(webdriver.Chrome):

    no_of_tabs = 0
    current_course = 3154

    def __init__(self, driver_path=const.get_user()['driver_path'], teardown=False, console=None):
        self.driver_path = driver_path
        self.teardown = teardown
        self.console = console
        super(Moodle, self).__init__(executable_path=driver_path)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
            pass

    def land_first_page(self):
        try:
            self.console.print('opening moodle...')
            self.get(const.BASE_URL)
            checkElem = self.find_element(
                by='xpath', value="//div[@id='frontpage-category-names']")

            if checkElem:
                self.console.print("login detected")
                self.find_element(
                    by='xpath', value="//span[@class='login']/a").click()
                self.console.print('clicked')
        except Exception as e:
            # print(e)
            self.console.error(type(e).__name__, exitN=True)

    def login(self):
        try:
            username = self.find_element(
                by='xpath', value="//input[@id='username']")

            password = self.find_element(
                by='xpath', value="//input[@id='password']")

            username.clear()
            username.send_keys(const.get_user()["id"])
            password.clear()
            password.send_keys(const.get_user()["pass"])

            self.console.print(
                f'login with id `'+const.COLORS['yellow'] + const.get_user()["id"] + const.COLORS['reset'] + '`')

            if username.text != const.get_user()["id"]:
                username.send_keys(Keys.BACK_SPACE * 18)

            self.find_element(
                by='xpath', value="//input[@name='submit']").click()
            self.console.print('login done')
        except Exception as e:
            # print(e)
            self.console.error(type(e).__name__, exitN=True)

    def open_course(self, course, new_win=False):
        if course in const.SUBJECTS:
            if new_win:
                self.next_window()
            self.find_element(
                by='xpath', value=f"//div[@class='w-100 text-truncate']/a[@href='https://courses.iiit.ac.in/course/view.php?id={const.SUBJECTS[course]}']").click()
            self.current_course = course
            self.console.print(
                const.COLORS['yellow'] + f'{course}' + const.COLORS['reset']+' opened')
        else:
            self.console.error(
                const.COLORS['yellow'] + f'{course}' + const.COLORS['reset']+' does not exist')

    def next_window(self, url='https://courses.iiit.ac.in/my/'):
        self.execute_script(f'''window.open('{url}');''')
        self.no_of_tabs = len(self.window_handles)-1
        self.switch_to.window(self.window_handles[self.no_of_tabs])
        pass

    def grade(self, course):
        if course in const.SUBJECTS:
            try:
                self.find_element(
                    by='xpath', value=f"//a[@id='action-menu-toggle-1']").click()
                self.find_element(
                    by='xpath', value=f"//a[@href='https://courses.iiit.ac.in/grade/report/overview/index.php']").click()
                self.find_element(
                    by='xpath', value=f"//a[contains(@href,'mode=grade&id={const.SUBJECTS[course]}')]").click()
                self.console.print(
                    'opened grades for ' + const.COLORS['yellow'] + f'{course}' + const.COLORS['reset'])
            except Exception as e:
                self.console.error(type(e).__name__, exitN=True)
        else:
            self.console.error(
                const.COLORS['yellow'] + f'{course}' + const.COLORS['reset']+' does not exist')

    def get_instance(self, course, inst: list):
        if course in const.SUBJECTS:
            try:
                inst_elements = self.find_elements(
                    by='xpath', value=f"//span[@class='instancename']")

                inst_names = [element.get_attribute('innerHTML').split('<')[
                    0] for element in inst_elements]

                if len(inst) == 1:
                    self.console.print(
                        'getting instances for ' + const.COLORS['yellow'] + f'{course}' + const.COLORS['reset'])
                    for element in inst_names:
                        print(' '*(len(self.console.get_timestamp())+3), element)

                elif len(inst) == 2:
                    temstr = inst[1]
                    regex = '(.*)' + temstr.replace('_', '(.*)') + '(.*)'
                    flag = 0
                    for i in range(len(inst_elements)):
                        result = re.search(
                            pattern=regex, string=inst_names[i], flags=re.IGNORECASE)
                        if result:
                            inst_elements[i].click()
                            self.console.print(
                                'opening ' + const.COLORS['yellow'] + f'{inst_names[i]}' + const.COLORS['reset'] +
                                ' of ' + const.COLORS['yellow'] + f'{course}' + const.COLORS['reset'])
                            flag = 1
                            break
                    if not flag:
                        self.console.print(
                            'No instance ' + const.COLORS['yellow'] + f'{inst[1]}' + const.COLORS['reset'] +
                            ' in ' + const.COLORS['yellow'] + f'{course}' + const.COLORS['reset'])

            except Exception as e:
                self.console.error(type(e).__name__, exitN=True)
        else:
            self.console.error(
                const.COLORS['yellow'] + f'{course}' + const.COLORS['reset']+' does not exist')

    def check_inst(self, courses: list, i):
        if courses[i-1] not in const.SUBJECTS:
            j = i
            while j >= 0:
                if courses[j] in const.SUBJECTS:
                    self.next_window()
                    self.open_course(courses[j])
                j -= 1
