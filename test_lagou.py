from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time
import csv
import unittest

class test_lagou(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dr = webdriver.Chrome()
        cls.dr.get("https://www.lagou.com/")
        cls.dr.maximize_window()
        cls.name ="测试开发"
        cls.dr.implicitly_wait(10)
        cls.listAll = []
        cls.list = []
        cls.now_time = time.strftime("%Y_%m_%d_%H_%M_%S")


    def WriteCsvFile(self,listAll):
        #异常处理
        csvFile2 = open(str(self.now_time)+".csv", 'w', newline='')  # 设置newline，否则两行之间会空一行
        writer = csv.writer(csvFile2)
        m = len(listAll)
        for i in range(m):
            writer.writerow(listAll[i])
        csvFile2.close()

    def by_id(self,id,action,key=None):
        try:
            if action == "click":
                self.dr.find_element_by_id(id).click()
            if action == "send_keys":
                self.dr.find_element_by_id(id).send_keys(key)
            if action =="clear":
                self.dr.find_element_by_id(id).clear()
        except Exception as e:
            print("未找到%s"%(id))

    def GetInfo(self):
        try:
            jobs_name = self.dr.find_elements_by_xpath("//div/a/h3")
            jobs_address = self.dr.find_elements_by_xpath("//span[@class='add']/em")
            jobs_money_require = self.dr.find_elements_by_xpath("//div[@class='p_bot']/div[@class='li_b_l']")
        except NoSuchElementException:
            self.dr.quit()
        else:
            return jobs_name, jobs_address, jobs_money_require

    # 点击下一页
    def next_page(self):
        try:
            next_page = self.dr.find_element_by_xpath("//span[@class='pager_next ']")
        except NoSuchElementException as e:
            print(e)
        ActionChains(self.dr).move_to_element(next_page).perform()
        time.sleep(2)
        next_page.click()

    def PageCount(self):
        # 可异常处理，可参数化
        total_pages = self.dr.find_elements_by_class_name("pager_not_current")[-1].text
        if total_pages is None:
            total_pages=1
        return int(total_pages)

    def SetElements(self):
        #可异常处理，可参数化
        self.len = len(self.dr.find_elements_by_class_name("position_link"))
        if self.list is None:
            self.list = 1
        return int(self.len)

    def click_element(self,i):
        #可以加异常处理,可参数化
        self.dr.find_elements_by_xpath("//div/a/h3")[i].click()


    def test_lagou_element(self):

        time.sleep(2)
        #关闭弹出框
        #if self.by_id("cboxOverlay","click"):
        self.by_id("cboxClose","click")
        #清空input
        self.by_id("search_input","clear")
        time.sleep(2)
        #输入测试开发
        self.by_id("search_input","send_keys",self.name)
        time.sleep(5)
        self.by_id("search_button","click")
        time.sleep(2)
        #获取分页最大值
        pagecount = self.PageCount()

        time.sleep(2)
        #获得页面数据行数
        self.len = self.SetElements()


        #获取当前页面句柄
        ch = self.dr.current_window_handle

        #遍历数据
        for page in range(pagecount-28):

            # 获取页面信息
            jobs_name, jobs_address, jobs_money_require = self.GetInfo()

            for i in range(self.len-13):

                job_name = jobs_name[i].text  # 职位
                job_address = jobs_address[i].text.split("·")[0]  # 城市
                info = jobs_money_require[i].text.split(' ')
                job_money = info[0]  # 薪资
                job_exper = info[1]  # 经验
                job_edu = info[3]  # 学历
                self.list.append(job_name)
                self.list.append(job_address)
                self.list.append(job_money)
                self.list.append(job_exper)
                self.list.append(job_edu)
                #判断名字中是否含有测试开发字样，如果有，点击文字
                if self.name in job_name:

                    self.click_element(i)

                    handles = self.dr.window_handles

                    self.dr.switch_to.window(handles[1])

                    time.sleep(5)
                    #获得职位描述
                    job_detail = self.dr.find_element_by_class_name("job_detail").text

                    self.list.append(job_detail)

                    time.sleep(3)
                    #关闭当前页
                    self.dr.close()

                    self.dr.switch_to.window(ch)

                    self.listAll.append(self.list)

                    self.list = []

                    time.sleep(3)

            self.next_page()

            time.sleep(10)

        self.WriteCsvFile(self.listAll)

    @classmethod
    def tearDownClass(cls):
        cls.dr.quit()

if __name__ == '__main__':
    unittest.main()