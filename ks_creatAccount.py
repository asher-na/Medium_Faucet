import code
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import gspread
import random
import platform
import pyperclip

sysOS = platform.system()
options = webdriver.ChromeOptions()
if (sysOS == 'Windows'):
    _chromedriver = '../driver/window_chromedriver' #chromedriver 위치에 따라 변경해야 함
    print('Windows')
else:
    _chromedriver = '../driver/chromedriver' #chromedriver 위치에 따라 변경해야 함
    print('MacOS')

driver = webdriver.Chrome(_chromedriver)

#=======================공통 변수============================
#구글 스프레드 시트 위치: https://docs.google.com/spreadsheets/d/1NVGssWH9tl_X7HW2Rwpff8M4INiTSQSfSvGayinUD6E/edit#gid=0
gs = gspread.service_account(filename="../google/sheetkey.json") #참조할 구글시트에 공유 되어있는 json 파일 추가
sh = gs.open("KStadium_Account").worksheet("Account")
ks_url = 'http://3.38.193.183:3000/auth/signup'
yop_url = 'https://yopmail.com/en/'

#============================================================================================================================================
# KStadium
#============================================================================================================================================

class ElementFind:
    def element_find(element, input_value):
        input_values = driver.find_elements(By.XPATH, "//input[@class='native-input sc-ion-input-ios']")
        for el in input_values:            
            if(el.get_attribute('name')==element):                
                el.send_keys(input_value)
                #print(element)
                break

class Kstadium:

    def Sign_in():
        driver.get(ks_url)
        driver.execute_script('window.open("https://yopmail.com/en/");')
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

        for start in range(3, 5):     
            # 엑셀 값 지정
            id = sh.acell('B' + str(start)).value
            name = sh.acell('C' + str(start)).value
            pw = sh.acell('D' + str(start)).value
            email = sh.acell('E' + str(start)).value
            
            ElementFind.element_find('userId', id) # id 입력
            time.sleep(1)

            driver.find_element(By.XPATH, '//*[@id="btnCheckIdDuplication"]').click() # ID Confirm
            time.sleep(2)

            ElementFind.element_find('name', name) # name 입력
            time.sleep(1)

            ElementFind.element_find('password', pw) # pw 입력
            time.sleep(1)

            ElementFind.element_find('passwordConfirm', pw) # pw 입력
            time.sleep(1)

            ElementFind.element_find('email', email) # email 입력
            time.sleep(1)

            try:
                activate_button = driver.find_element(By.XPATH, '//*[@id="btnSendAuthEmail"]') # Activate 버튼 클릭
                if activate_button.is_enabled:
                    activate_button.click()
                    time.sleep(5)
            except(ElementClickInterceptedException):
                print('email 입력.')
                time.sleep(5)
                break

            ### yopmail 전환
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(5)
            driver.find_element(By.XPATH, '//*[@id="login"]').clear()
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(id) #id입력
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="refresh"]/i').click()
            time.sleep(5)
            
            
            time.sleep(5)

            #iframe 으로 전환 (본문)
            driver.switch_to.frame('ifmail')
            full_code = driver.find_element(By.XPATH, '//*[@id="mail"]').text
            code = full_code[12:18]
            #frame 복귀
            driver.switch_to.default_content()

            #yopmail Main 화면으로 전환
            driver.find_element(By.XPATH, '//*[@id="webmail"]/div[1]/header/div/div[1]/a').click()
            time.sleep(2)      

            driver.switch_to.window(driver.window_handles[0]) #KStadium 전환
            time.sleep(5)

            ElementFind.element_find('emailAuthCode', code) # email code 입력
            time.sleep(1)

            try:
                confirm_button = driver.find_element(By.XPATH, '//*[@id="btnCheckEmailAuthCode"]')
                if confirm_button.is_enabled():
                    confirm_button.click()
                    time.sleep(3)

            except(ElementClickInterceptedException):
                print('인증코드 입력.')
                time.sleep(1)
                break

            input_box = driver.find_element(By.XPATH, '//*[@id="chkAgreePolicy"]').click() # 동의 체크
            time.sleep(2)
        
            driver.find_element(By.XPATH, '//*[@id="btnSignUpSubmit"]').click() # CREATE ACCOUNT 버튼 클릭
            time.sleep(3)
            sh.update_acell('F' + str(start), 'OK')

            #Sign up 화면 재 진입을 위한 과정
            driver.find_element(By.XPATH, '//*[@id="btnSignIn"]').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="lnkSignUp"]').click()
            time.sleep(5)

Kstadium.Sign_in()