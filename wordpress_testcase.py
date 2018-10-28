from selenium import webdriver
import time
import unittest

class wordpress_testcase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dr = webdriver.Chrome()
        cls.dr.get("http://139.199.192.100:8000/wp-login.php")
        cls.dr.maximize_window()
        cls.dr.implicitly_wait(10)
        cls.username ='pyse17'
        cls.password ='pyse17'

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()

    def test_a_login_success(self):
        '''登录生成'''
        self.dr.find_element_by_id("user_login").send_keys(self.username)
        self.dr.find_element_by_id("user_pass").send_keys(self.password)
        self.dr.find_element_by_id("wp-submit").click()
        text = self.dr.find_element_by_css_selector("#wp-admin-bar-my-account > a > span").text
        time.sleep(2)
        url = self.dr.current_url
        print(text)
        print(url)
        self.assertIn(text,self.username)
        self.assertEqual(url,"http://139.199.192.100:8000/wp-admin/")

    def test_b_add_article(self):
        '''创建文章'''
        title = "新建文章%s" %(time.time())
        self.dr.find_element_by_link_text("新建").click()
        self.dr.find_element_by_name("post_title").send_keys(title)
        self.set_content("文章内容%s " %(time.time()))

        self.dr.find_element_by_id("publish").click()

        self.dr.get("http://139.199.192.100:8000/wp-admin/edit.php")

        edit_page_title = self.dr.find_element_by_css_selector(".row-title").text

        print(edit_page_title.strip())

        self.assertEqual(edit_page_title.strip(),title)

    def test_c_delete_article(self):
        '''删除文章'''
        edit_page_title = self.dr.find_element_by_css_selector(".row-title").text

        self.dr.find_element_by_css_selector(".row-title").click()

        self.dr.find_element_by_css_selector("#delete-action > a").click()

        self.dr.get("http://139.199.192.100:8000/wp-admin/edit.php")

        page_title = self.dr.find_element_by_css_selector(".row-title").text

        print(edit_page_title.strip())

        self.assertNotEqual(edit_page_title, page_title)

    def set_content(self, text):
        js = 'document.getElementById("content_ifr").contentWindow.document.body.innerHTML="%s"' % (text)
        print(js)
        self.dr.execute_script(js)


if __name__ == '__main__':
    unittest.main()
