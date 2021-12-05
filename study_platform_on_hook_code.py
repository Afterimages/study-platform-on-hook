#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver


# In[ ]:


from selenium.webdriver.common.keys import Keys


# In[ ]:


from selenium.webdriver.support import expected_conditions as EC


# In[ ]:


import time
import os


# In[ ]:


options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")


# In[ ]:


driver = webdriver.Chrome(options=options)


# In[ ]:


url = "https://study.enaea.edu.cn/login.do;jsessionid=64C3D842FE40C8AC865A49D89542074B.web55"
driver.get(url) 


# In[ ]:


driver.refresh()
print('已进入登录页面。')


# In[ ]:


with open("account_password_record.txt","a+",encoding = "utf_8") as f:
    if os.stat("account_password_record.txt").st_size==0:
        print("程序检测到您没有上次登录的保存记录，请输入以下信息。")
        print('请输入您的账号：')
        account_text = input()
        f.write(account_text)
        f.write("\n")
        print("请输入您的密码：")
        password_text = input()
        f.write(password_text)
        print("已保存您的账号密码，下次打开程序时将自动登录。（只要您别把account_password_record.txt文件删除或者移动到非法目录）")
    else:
        f.close()
        with open("account_password_record.txt","r",encoding = "utf_8") as f:
            account_text = f.readline()
            password_text = f.readline()


# In[ ]:


print("登录记录中您的账号为：")
print(account_text)


# In[ ]:


print("您的密码为：")
print(password_text)
print("请检查是否有误,如果有误，请中断程序后修改账号密码。")


# In[ ]:


account = driver.find_element_by_name('username')
account.send_keys(account_text)
time.sleep(2)


# In[ ]:


password = driver.find_element_by_name('password')
password.send_keys(password_text)


# In[ ]:


button_log_in = driver.find_element_by_class_name('btn-row')
button_log_in.click()
time.sleep(3)


# In[ ]:


print("登录成功！")


# In[ ]:


button_log_in = driver.find_element_by_id('J_submitReg')
button_log_in.click()
time.sleep(2)


# In[ ]:


print("正在切换窗口。")


# In[ ]:


button_log_in = driver.find_element_by_css_selector('.button.intoStudy')
button_log_in.click()


# In[ ]:


print("进入学习界面成功！")


# In[ ]:


time.sleep(2)


# In[ ]:


def refresh_window_handles():
    all_handles = driver.window_handles
    driver.switch_to.window(all_handles[-1])


# In[ ]:


refresh_window_handles()


# In[ ]:


print("跳转窗口倒计时：")
for i in range(3):
    print(3-i)
    time.sleep(1) 


# In[ ]:


button_log_in = driver.find_element_by_link_text("查看")
button_log_in.send_keys(Keys.ENTER) 


# In[ ]:


refresh_window_handles()
print('已跳转到查看窗口。')


# In[ ]:


time.sleep(2)


# In[ ]:


def watchvideo_click(i):
    try:
        path = '/html/body/div[4]/div[2]/div/div/div[3]/div/table/tbody/tr[{}]/td[6]/a'.format(i)
        button_video = driver.find_element_by_xpath(path)
    except:
        return 0
    else:
        button_video.send_keys(Keys.ENTER) 
        refresh_window_handles()
        return 1


# In[ ]:


def progress_text(ch):
    progress_path = "/html/body/div[2]/div/div[2]/div[1]/ul/li[1]/div[2]/ul/li[{}]/div/div[2]".format(ch)
    progress = driver.find_element_by_xpath(progress_path)
    text = int(progress.text.split('%')[0])
    return text


# In[ ]:


def progress_check(i):
    ch = 1
    while ch<10:
        try:
            text = progress_text(ch)           
        except:
            ch=0 
            print("本章节已播放完毕！准备进入下一章节！")
            return ch
        else:
            print("第{}集的进度为{}%！".format(ch,text))
            if text<100:
                check = 1              
                return ch
            ch +=1  


# In[ ]:


def progress_button_click(ch):
    character_path = "/html/body/div[2]/div/div[2]/div[1]/ul/li[1]/div[2]/ul/li[{}]/div/div[3]".format(ch)
    driver.find_element_by_xpath(character_path).click()
    print("跳转播放！")


# In[ ]:


def stop_check(ch):
    t1 = progress_text(ch)
    time.sleep(120)
    t2 = progress_text(ch)
    if t1==t2:
        print("由于网络等问题停止播放。。。重新加载中！")        
        refresh_window_handles()
        time.sleep(3)
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div/section/span[1]").click() 


# In[ ]:


def alertlike_check_and_click(i,ch):
    num=10
    time.sleep(1000)
    while (num):
        refresh_window_handles()
        try:
            al = driver.find_element_by_xpath("/html/body/div[6]/table/tbody/tr[2]/td[2]/div[3]/button")            
        except:
            time.sleep(5)           
            if progress_check(i)==0:
                all_handles =driver.window_handles 
                driver.switch_to.window(all_handles[1])
                break
            stop_check(ch)
        else:
            al.click()
            num=num-1
            print("出现第{}个弹窗,已确认。".format(10-num))
            ##print(num)
            time.sleep(1200)


# In[ ]:


def turn_page():
    time.sleep(3)
    driver.find_element_by_css_selector(".next.paginate_button").click()


# In[36]:


try:
    page = 1
    all_handles =driver.window_handles 
    driver.switch_to.window(all_handles[1])
    while (4-page):
        for i in range(2,23):
            if watchvideo_click(i)==0:
                continue
            time.sleep(2)
            ch = progress_check(i)
            if ch:
                progress_button_click(ch)
            else:
                all_handles =driver.window_handles 
                driver.switch_to.window(all_handles[1])
                continue
            alertlike_check_and_click(i,ch)
        print("第{}页已播放完毕！".format(page))
        turn_page()
        page +=1
        if(page<4):
            print("跳转至第{}页！".format(page))
except:
    driver.quit()
    print("程序异常！已结束进程！请检查是否有非法操作。比如账号密码错误，人为切换窗口，关闭浏览器等等，如果出现代码问题请联系博主")
else:
    driver.quit()
    print("正常结束进程")


# In[ ]:




