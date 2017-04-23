from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver import Chrome
from selenium.webdriver.support.select import Select


class FunctionalTest(StaticLiveServerTestCase):
    browser = Chrome()

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        cls.browser.get(cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        super(FunctionalTest, cls).tearDownClass()
        cls.browser.close()

    def __create_page(self, content, x, y, z, rx, ry, rz, scale):
        # 用户输入了一些数据
        self.browser.find_element_by_id('content').send_keys(content)
        self.browser.find_element_by_id('x').send_keys(str(x))
        self.browser.find_element_by_id('y').send_keys(str(y))
        self.browser.find_element_by_id('z').send_keys(str(z))
        self.browser.find_element_by_id('rx').send_keys(str(rx))
        self.browser.find_element_by_id('ry').send_keys(str(ry))
        self.browser.find_element_by_id('rz').send_keys(str(rz))
        self.browser.find_element_by_id('scale').send_keys(str(scale))
        # 用户点击了确定
        self.browser.find_element_by_id('add-or-edit-page').click()
        self.browser.implicitly_wait(0.1)

    def __assert_page_exist(self, page_id, content, x, y, z, rx, ry, rz, scale):
        self.browser.switch_to.frame('impress-frame')
        self.assertInHTML(
            '''
            <div id="step-''' + str(page_id) + '''"
                class="step present active"
                data-x="''' + str(x) + '''" data-y="''' + str(y) + '''" data-z="''' + str(z) + '''"
                data-rotate-x="''' + str(rx) + '''" data-rotate-y="''' + str(ry) + '''" data-rotate-z="''' + str(rz) + '''"
                data-scale="''' + str(scale) + '''"
                data-raw-content="''' + str(content) + '''"
                style="position: absolute; transform: translate(-50%, -50%) translate3d(''' + str(x) + '''px, ''' + str(
                y) + '''px, ''' + str(z) + '''px) rotateX(''' + str(rx) + '''deg) rotateY(''' + str(
                ry) + '''deg) rotateZ(''' + str(rz) + '''deg) scale(''' + str(scale) + '''); transform-style: preserve-3d;">
                    ''' + str(content) + '''
            </div>
            ''', self.browser.page_source)
        self.browser.switch_to.parent_frame()

    def check_basic_ui(self):
        # 用户看见了控制面板
        try:
            self.browser.find_element_by_id('control-panel')
        except NoSuchElementException:
            self.fail('Please add a control panel')
            # 用户看见了控制面板
        try:
            self.browser.find_element_by_id('presentation-name')
        except NoSuchElementException:
            self.fail('Please add a presentation-name input')
        # 用户看见了demo的网页效果
        try:
            self.browser.switch_to.frame('impress-frame')
            self.browser.switch_to.parent_frame()
        except NoSuchFrameException:
            self.fail('Please add a impress-frame')

    def check_set_page_title(self):
        self.browser.find_element_by_id('presentation-name').send_keys('demo')
        self.assertIn('demo', self.browser.title)

    def check_can_create_page(self):
        # 用户新建了一个Page
        self.__create_page('Hello world', 100, 200, 300, 15, 30, 45, 2)
        sleep(1)
        # 用户从demo页面上看见了自己的新页面
        self.__assert_page_exist(1, 'Hello world', 100, 200, 300, 15, 30, 45, 2)
        self.browser.switch_to.parent_frame()
        # 用户从列表中看见了自己的新页面
        self.assertInHTML('<option value="1">(100,200,300)Hello worl...</option>',
                          self.browser.find_element_by_id('page-select').get_attribute('innerHTML')
                          )
        # 用户又新建了一个Page
        self.__create_page('Goodbye world', 1000, 0, 0, 0, 90, 0, 1)
        sleep(2)
        # 用户又从demo页面上看见了自己的新页面
        self.__assert_page_exist(2, 'Goodbye world', 1000, 0, 0, 0, 90, 0, 1)
        self.browser.switch_to.parent_frame()
        # 用户从列表中看见了自己的新页面
        self.assertInHTML('<option value="2">(1000,0,0)Goodbye wo...</option>',
                          self.browser.find_element_by_id('page-select').get_attribute('innerHTML'))

    def check_can_switch_page(self):
        Select(self.browser.find_element_by_id('page-select')).select_by_value('1')
        sleep(2)
        # 用户从列表中看见了第一个页面
        self.assertInHTML('<option value="1">(100,200,300)Hello worl...</option>',
                          self.browser.find_element_by_id('page-select').get_attribute('innerHTML')
                          )
        # 用户在侧栏编辑区看到的是第一个页面的数据
        self.assertEqual('Hello world', self.browser.find_element_by_id('content').get_attribute('value'))
        self.assertEqual('100', self.browser.find_element_by_id('x').get_attribute('value'))
        self.assertEqual('200', self.browser.find_element_by_id('y').get_attribute('value'))
        self.assertEqual('300', self.browser.find_element_by_id('z').get_attribute('value'))
        self.assertEqual('15', self.browser.find_element_by_id('rx').get_attribute('value'))
        self.assertEqual('30', self.browser.find_element_by_id('ry').get_attribute('value'))
        self.assertEqual('45', self.browser.find_element_by_id('rz').get_attribute('value'))
        self.assertEqual('2', self.browser.find_element_by_id('scale').get_attribute('value'))
        # 用户在demo页面上看见的也是第一个页面
        self.__assert_page_exist(1, 'Hello world', 100, 200, 300, 15, 30, 45, 2)

    def check_can_remove_page(self):
        Select(self.browser.find_element_by_id('page-select')).select_by_value('-1')
        sleep(1)
        # 用户新建了一个Page
        self.__create_page('Goodbie world', 2000, 0, 0, 0, 90, 0, 1)
        sleep(2)
        self.__assert_page_exist(3, 'Goodbie world', 2000, 0, 0, 0, 90, 0, 1)
        # 用户对这个page 不太满意，他要删除它
        Select(self.browser.find_element_by_id('page-select')).select_by_value('3')
        self.browser.find_element_by_id('remove-page').click()
        sleep(2)
        # 这个Page不再出现了
        with self.assertRaises(AssertionError):
            self.__assert_page_exist(3, 'Goodbie world', 2000, 0, 0, 0, 90, 0, 1)
        self.browser.switch_to.parent_frame()
        # 用户不再能从列表中看见第二个页面
        with self.assertRaises(AssertionError):
            self.assertInHTML('<option value="3">(2000,0,0)Goodbie wo...</option>',
                              self.browser.find_element_by_id('page-select').get_attribute('innerHTML')
                              )

    def check_can_edit_page(self):
        Select(self.browser.find_element_by_id('page-select')).select_by_value('1')
        sleep(2)
        self.browser.find_element_by_id('x').clear()
        self.browser.find_element_by_id('x').send_keys(0)
        self.assertEqual('Edit', self.browser.find_element_by_id('add-or-edit-page').text)
        self.browser.find_element_by_id('add-or-edit-page').click()
        sleep(2)
        self.__assert_page_exist(1, 'Hello world', 0, 200, 300, 15, 30, 45, 2)
        self.assertInHTML('<option value="1">(0,200,300)Hello worl...</option>',
                          self.browser.find_element_by_id('page-select').get_attribute('innerHTML')
                          )
        Select(self.browser.find_element_by_id('page-select')).select_by_value('-1')
        self.assertEqual('Add', self.browser.find_element_by_id('add-or-edit-page').text)

    def test_all(self):
        self.check_basic_ui()
        self.check_set_page_title()
        self.check_can_create_page()
        self.check_can_switch_page()
        self.check_can_remove_page()
        self.check_can_edit_page()
