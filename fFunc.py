# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import gspread
import random


options = webdriver.ChromeOptions()
_chromedriver = '/Users/medium/python/chromedriver' #chromedriver 위치에 따라 변경해야 함
packed_extension_path = '/Users/medium/python/olkbchllhcflpbjfgagahpkjnjioiedg.zip' #chrome extension 위치에 따라 변경해야 함
options.add_extension(packed_extension_path)
driver = webdriver.Chrome(_chromedriver, options=options)

#============================================================================================================================================
#               변수 리스트
#============================================================================================================================================

#=======================공통 변수============================
#구글 스프레드 시트 위치: https://docs.google.com/spreadsheets/d/1NVGssWH9tl_X7HW2Rwpff8M4INiTSQSfSvGayinUD6E/edit#gid=0
gs = gspread.service_account(filename="./sheetkey.json") #참조할 구글시트에 공유 되어있는 json 파일 추가
sh = gs.open("Faucet_auto").worksheet("faucet_send")

#Test를 위해 생성해놓은 계정 주소와 그에따른 Seed 구문
#wallet 계정 변경 시 구글 시트에서 주소를 참조해 아래 주소와 비교하여 seed 구문을 가져오도록 되어 있음
adress_seed = {"0x1914627a35cf0822714f79D2584b278F92fC8be5":"bind orbit account repeat buddy sad clog property vapor cake raven original",
            "0xF6ef8923316B3D12C8fb537EFd486059427a1c7D":"tower boost ready buddy task sudden lake lemon charge hamster capital organ",
            "0x4c7eD9DA6b7f123b70E55519020268B03C9247D7":"mixed distance resemble valve saddle message post pledge acid nurse spider absorb",
            "0xcBe046c536AC02A12123017269f0D2439CdD0774":"heart endorse abstract caught cave edit rebel rain steak organ lyrics stomach",
            "0x81b3E378eDEeA4C1D9fBaC70F0148755B74Ac16a":"fantasy dune decorate stuff fetch poet tornado place gown gasp gesture motion",
            "0xeE057c636d3822B949Ed3BAA59E683F69206435b":"review ceiling fresh yellow guard vicious pole match bronze claw spawn measure",
            "0xDFf052e718Da3F031be03BDC96133A0289F0C115":"mean demise deny exotic average stumble list silly visa floor wisdom equal",
            "0x5c6cF77f0Aa6653b1f3c18ee898AcD8feB7Cb8a5":"laundry spirit defense doll fall rhythm solution more profit retreat cattle vibrant",
            "0x97a43358AB8D71359149Dc4296c4E22e804Dc0d5":"scatter lion acoustic error able pill service spot budget pattern absent father",
            "0xA218471bB241A55506E471bD041716ca87E50f30":"knife matrix waste begin abstract tennis bundle off edge credit fade draft"}

#Faucet에서 설정한 토큰과 그에따른 wallet 네트워크 이름
#{'Faucet 토큰명':'wallet 네트워크 이름'}
token_net = {'besu':'besu', 'mdl':'mdl', 'erc20':'Ropsten 테스트 네트워크'}

# while문 사용시 함수안에 count 증가 시키기위한 변수
count = 0 
a = 0
def counta(type, *args):            
    type == 'count'
    count = 0    
    for i in args:
        count = count + i        
        if type == 'count':
            return count             

#=======================Faucet 변수============================
#Faucet 주소
url = 'http://54.180.99.44/'

#Faucet 전송시 Alert 종류
id = ['red', 'blue', 'blue-leak', 'red-etc', 'green']

#Alert 발생시 구글 스프레드시트 or 출력 데이터에 입력할 양식 
comment = ['예)주소입력 오류', '예)주소 입력 오류로 인해 전송 실패', '예)주소 입력 오류로 인해']

#=======================Wallet 변수============================
#지갑 비밀번호
password = 'vnfmsgk12#'

# besu 네트워크 생성
network_name = 'besu'
rpc_url = 'http://13.124.209.160:8545'
chain_id = '2018'
sign = 'MDM'

# mdl 네트워크 생성
network_name1 = 'mdl'
rpc_url1 = 'http://13.124.149.73:8545/api'
chain_id1 = '18'
sign1 = 'MDM'

#============================================================================================================================================
#               Wallet 설정 
#============================================================================================================================================

class wallet:    
    # faucet url과 지갑 화면 노출시키기
    def extention():
        time.sleep(2)
        # faucet 화면으로 전환
        if (len(driver.window_handles) > 1):
            # faucet url 가져오기
            driver.get(url)
            #지갑 화면으로 전환
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    #기존에 생성했던 지갑 가져오기
    def importwallet():
        time.sleep(1)
        # 시작하기 버튼 클릭
        start = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button').click()

        # 지갑가져오기 버튼 클릭
        time.sleep(1)
        importwallet = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[2]/div/div[2]/div[1]/button').click()

        # 동의하기 버튼 클릭
        time.sleep(1)
        agree = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[5]/div[1]/footer/button[2]').click()

        #시드 그문 text 가져오기
        #time.sleep(1)
        #seedfile = open('/Users/medium/python/seed.txt', 'rt')
        #seedtext = seedfile.readlines()
        #seedfile.close()

        #시드 구문 입력
        time.sleep(1)
        seedinput = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[3]/div[1]/div/input[contains(@dir, "auto")]')
        #시드구문 가져오기 / adress_seed에 입력한 주소를 가져와 그에 해당하는 seed 구문을 출력한다
        seedinput.send_keys(adress_seed["0x1914627a35cf0822714f79D2584b278F92fC8be5"])

        #시드 구문 표시버튼 클릭
        time.sleep(1)
        seeddisply = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[3]/div[2]/div[contains(@role, "checkbox")]')
        seeddisply.click()

        #암호 입력
        time.sleep(1)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(1)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('confirm-password').send_keys(password)

        #이용약관 클릭
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[6]/div').click()

        #가져오기 버튼 활성화 확인
        nextBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/button[2]')
        backBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[7]/button[1]')
        isExistNextPage = nextBtn.is_enabled()

        # 다음 버튼이 비활성화 이면 "잘못된 시드구문" 출력, 
        if (isExistNextPage == False):            
            try:
                driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/form/div[3]/span')
                print('===잘못된 시드구문===')
            # 다음 버튼이 비활성화이고 시드구문에 잘못이 없으면 "잘못된 비밀번호" 출력, 
            except NoSuchElementException:
                driver.find_element_by_xpath('//*[@id="confirm-password-helper-text"]')
                print('====잘못된 비밀번호===')
        # 다음 버튼이 활성화 이면 다음버튼 클릭
        else:
            nextBtn.click()

        # 축하화면에서 모두완료 버튼 클릭
        time.sleep(2)
        finish = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/button').click()


    #새 네트워크 생성하기 / 매개변수에 원하는 변수를 넣어 네트워크 입력시 활용
    def settingnet(network_name, rpc_url, chain_id, sign):
        #Account menu 클릭하여 설정 진입
        time.sleep(1)
        driver.find_element_by_xpath("//*[@class='identicon__address-wrapper']").click()
        driver.find_element_by_xpath("//*[@class='account-menu__item__text']").click()

        #설정에 네트워크 항목 진입
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='app-content']/div/div[4]/div/div[2]/div[1]/div/button[6]/div[1]/div[1]").click()

        #네트워크 추가 버튼 클릭
        time.sleep(1)
        driver.find_element_by_xpath("//*[@class='button btn-secondary']").click()

        # 네트워크 입력 / 각 변수에 저장된 데이터를 가져와서 대입
        time.sleep(1)
        networkID = driver.find_element_by_xpath("//*[@id='network-name']").send_keys(network_name)
        time.sleep(1)
        rpcURL = driver.find_element_by_xpath("//*[@id='rpc-url']").send_keys(rpc_url)
        time.sleep(1)
        chainID = driver.find_element_by_xpath("//*[@id='chainId']").send_keys(chain_id)
        time.sleep(1)
        ticker = driver.find_element_by_xpath("//*[@id='network-ticker']").send_keys(sign)

        # 저장버튼 클릭
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/div[7]/button[2]').click()

        #설정화면 빠져나와 홈화면 진입하기
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div[1]/div[3]').click()

    # 지갑 계정 복구(변경)하기
    def changewallet():        
        #Account menu 진입하여 잠금 버튼 클릭 
        time.sleep(1)
        driver.find_element_by_xpath("//*[@class='identicon__address-wrapper']").click()
        driver.find_element_by_xpath("//*[@class='account-menu__lock-button']").click()

        # 계정을 복구하시겠습니까 버튼 클릭
        time.sleep(1)
        driver.find_element_by_xpath("//*[@class='unlock-page__link text-light-gray']").click()

        #시드 구문 입력하기
        time.sleep(1)
        seedinput = driver.find_element_by_xpath("//*[@id='app-content']/div/div[4]/div/div/div/div[3]/div[1]/div/input")
        #adress_seed에 입력된 주소를 가져와서 그에따른 seed 구문 호출
        seedinput.send_keys(adress_seed["0x1914627a35cf0822714f79D2584b278F92fC8be5"])

        #시드 구문 표시
        time.sleep(1)
        seeddisply = driver.find_element_by_xpath('//*[@id="seed-checkbox"]')
        seeddisply.click()

        #암호 입력
        time.sleep(1)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(1)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('confirm-password').send_keys(password)

        #복구 버튼 활성화 확인
        nextBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[2]')
        backBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[1]')
        isExistNextPage = nextBtn.is_enabled()

        # 다음 버튼이 비활성화 이면 "잘못된 시드구문" 출력, 
        if (isExistNextPage == False):
            try:
                driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/span')        
                print('===잘못된 시드구문===')
            
            # 다음 버튼이 비활성화이고 시드구문에 잘못이 없으면 "잘못된 비밀번호" 출력, 
            except NoSuchElementException:
                driver.find_element_by_xpath('//*[@id="confirm-password-helper-text"]')
                print('====잘못된 비밀번호===')

        # 다음 버튼이 활성화 이면 다음버튼 클릭
        else:
            nextBtn.click()

        time.sleep(2)
        #미디움 로고 클릭하여 홈화면 노출
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[1]/img[1]').click()


    # 네트워크 목록에서 원하는 네트워크로 변경하기
    def  changenet():
        # 네트워크 변경
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='app-content']/div/div[1]/div/div[2]/div[1]/div/span").click()
        # token_net에 입력된 토큰을 가져와서 그에따른 네트워크 호출
        action = ActionChains(driver)
        submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{}")]'.format(token_net['besu']))))
        action.move_to_element(submenu).click().perform()

    #설정한 주소에 해당하는 토큰 자산 노출 시키기
    def checkasset():        
        # 현재 자산 노출하기
        time.sleep(2)
        # 현재 지갑의 주소
        adressinfo = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        mdmasset = driver.find_elements_by_xpath("//*[@class='currency-display-component__text']")
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath("//*[@class='currency-display-component__suffix']")
        for asset in mdmasset:
            for curren in currency:
                print('현재 {0}주소의 자산은 {1}{2} 입니다.'.format(adressinfo.text, asset.text, curren.text))
                sh.update_cell((count + 2), 6, asset.text)
                #Faucet 화면으로 전환하기
                driver.switch_to.window(driver.window_handles[-1])


#============================================================================================================================================
#            Faucet 전송하기
#============================================================================================================================================

class faucet():
    #시간 측정하기
    def starttime():
        #현재 시간 측정
        now = datetime.datetime.now()
        #전송 시간(현재 시간) 노출 / %H:%M:%S 형식
        starttime = now.strftime('%H:%M:%S')
        print("전송 시작시간은 {} 입니다.".format(starttime))
        # 시작시간 측정 / 총 소요시간 측정을 위한 데이터    
        global start
        start = time.time() 

    #네트워크 변경하기
    def changenet():
        # while문 사용시 count 증가를 위한 조건 / counta 변수 사용
        global a
        a = a + 1        
        count = counta('count', a)

        # 토큰 데이터 가져오기 / count 증가에 따른 cell 데이터 추출
        # count = 1일 경우 3행 1열의 데이터 추출
        token = sh.cell((count + 2), 2).value
        
        # 테스트 목적을 확인하기 위한 데이터 가져오기 / 토큰 변경 유무 확인
        purpose = sh.cell(count + 2, 1).value

        # 구글시트에서 change_token, change_all 데이터를 가져오는 경우 wallet에서 네트워크를 변경
        if purpose == "change_token":
            # 네트워크 변경하기
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='app-content']/div/div[1]/div/div[2]/div[1]/div/span").click()
            action = ActionChains(driver)
            # 구글시트에서 token 값을 가져오고 그 값을 token_net 변수에 대입시켜 network 값을 추출
            submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{}")]'.format(token_net[token]))))
            action.move_to_element(submenu).click().perform()
            print('{}로 변경 했습니다.'.format(token_net[token]))

        elif purpose == "change_all":
            # 네트워크 변경하기
            time.sleep(1)
            dropmenu = driver.find_element_by_xpath("//*[@id='app-content']/div/div[1]/div/div[2]/div[1]/div/span").click()
            action = ActionChains(driver)
            # 구글시트에서 token 값을 가져오고 그 값을 token_net 변수에 대입시켜 network 값을 추출
            submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{}")]'.format(token_net[token]))))
            action.move_to_element(submenu).click().perform()
            print('{}로 변경 했습니다.'.format(token_net[token]))

        else:
            pass

    #지갑 계정(주소) 변경하기
    def changewallet():
        a
        count = counta('count', a)

        #구글 시트에서 주소 데이터 가져오기
        adress = sh.cell((count + 2), 3).value
        
        # 테스트 목적을 확인하기 위한 데이터 가져오기 / 주소 변경 유무 확인
        purpose = sh.cell(count + 2, 1).value

        # 구글시트에서 change_adress 데이터를 가져오는 경우 wallet에서 계정(주소) 변경하기
        if purpose == "change_adress":
            time.sleep(5)        
            
            # Account menu에서 잠금 버튼 클릭 
            time.sleep(1)
            driver.find_element_by_xpath("//*[@class='identicon__address-wrapper']").click()
            driver.find_element_by_xpath("//*[@class='account-menu__lock-button']").click()

            # 복구 버튼 누르기 
            time.sleep(1)
            driver.find_element_by_xpath("//*[@class='unlock-page__link text-light-gray']").click()

            #시드 구문 입력
            time.sleep(1)
            seedinput = driver.find_element_by_xpath("//*[@id='app-content']/div/div[4]/div/div/div/div[3]/div[1]/div/input")
            #시드구문 가져오기 / 구글 시트에서 가져온 adress 주소를 adress_seed 변수에 대입시켜 해당 주소에 맞는 seed 구문 호출
            seedinput.send_keys(adress_seed[adress])

            #시드 구문 표시
            time.sleep(1)
            seeddisply = driver.find_element_by_xpath('//*[@id="seed-checkbox"]')
            seeddisply.click()

            #새 암호 입력
            time.sleep(1)
            #비밀번호 가져오기 / password 변수값 가져오기
            newpassword = driver.find_element_by_id('password').send_keys(password)
            time.sleep(1)
            #비밀번호 가져오기 / password 변수값 가져오기
            checkpassword = driver.find_element_by_id('confirm-password').send_keys(password)

            #복구 버튼 활성화 확인
            nextBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[2]')
            backBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[1]')
            isExistNextPage = nextBtn.is_enabled()

            # 다음 버튼이 비활성화 이면 "잘못된 시드구문" 출력, 
            if (isExistNextPage == False):
                try:
                    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/span')        
                    print('===잘못된 시드구문===')
            
                # 다음 버튼이 비활성화이고 시드구문에 잘못이 없으면 "잘못된 비밀번호" 출력, 
                except NoSuchElementException:
                    driver.find_element_by_xpath('//*[@id="confirm-password-helper-text"]')
                    print('====잘못된 비밀번호===')

            # 다음 버튼이 활성화 이면 다음버튼 클릭
            else:
                nextBtn.click()

            time.sleep(2)
            #미디움 로고 클릭
            driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[1]/img[1]').click()

        # 구글시트에서 change_all 데이터를 가져오는 경우 wallet에서 계정(주소) 변경하기
        elif purpose == "change_all":
            time.sleep(5)        
            #구글 스프레드 시트 가져오기
            #주소에 맞는 지갑으로 변경
            #지갑 잠그기 
            time.sleep(1)
            driver.find_element_by_xpath("//*[@class='identicon__address-wrapper']").click()
            driver.find_element_by_xpath("//*[@class='account-menu__lock-button']").click()

            # 복구 버튼 누르기 
            time.sleep(1)
            driver.find_element_by_xpath("//*[@class='unlock-page__link text-light-gray']").click()

            #시드 구문 입력
            time.sleep(1)
            seedinput = driver.find_element_by_xpath("//*[@id='app-content']/div/div[4]/div/div/div/div[3]/div[1]/div/input")
            #시드구문 가져오기(변수)
            seedinput.send_keys(adress_seed[adress])

            #시드 구문 표시
            time.sleep(1)
            seeddisply = driver.find_element_by_xpath('//*[@id="seed-checkbox"]')
            seeddisply.click()

            #새 암호 입력
            time.sleep(1)
            #비밀번호 가져오기(변수)
            newpassword = driver.find_element_by_id('password').send_keys(password)
            time.sleep(1)
            #비밀번호 가져오기(변수)
            checkpassword = driver.find_element_by_id('confirm-password').send_keys(password)

            #복구 버튼 활성화 확인
            nextBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[2]')
            backBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[6]/button[1]')
            isExistNextPage = nextBtn.is_enabled()

            # 다음 버튼이 비활성화 이면 "잘못된 시드구문" 출력, 
            if (isExistNextPage == False):
                try:
                    driver.find_element_by_xpath('//*[@id="app-content"]/div/div[4]/div/div/div/div[3]/span')        
                    print('===잘못된 시드구문===')
            
                # 다음 버튼이 비활성화이고 시드구문에 잘못이 없으면 "잘못된 비밀번호" 출력, 
                except NoSuchElementException:
                    driver.find_element_by_xpath('//*[@id="confirm-password-helper-text"]')
                    print('====잘못된 비밀번호===')

            # 다음 버튼이 활성화 이면 다음버튼 클릭
            else:
                nextBtn.click()

            time.sleep(2)
            #미디움 로고 클릭
            driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[1]/img[1]').click()
        else:
            pass

    #Wallet 자산 노출 시키기
    def assetprint():
        a
        count = counta('count', a)      
        # 현재 자산 노출하기
        time.sleep(2)
        # 현재 지갑의 주소
        adressinfo = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        mdmasset = driver.find_elements_by_xpath("//*[@class='currency-display-component__text']")
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath("//*[@class='currency-display-component__suffix']")
        for asset in mdmasset:
            for curren in currency:
                print('현재 {0}주소의 자산은 {1}{2} 입니다.'.format(adressinfo.text, asset.text, curren.text))
                sh.update_cell((count + 2), 6, asset.text)
                break
        
        time.sleep(2)
        #Faucet 화면으로 전환
        driver.switch_to.window(driver.window_handles[-1])  
    
    #Faucet에서 토큰 전송하기
    def faucetsetting():
        a   
        count = counta('count', a)
        # 구글 시트에서 토큰 및 주소 데이터 추출
        token = sh.cell((count + 2), 2).value
        adress = sh.cell((count + 2), 3).value
        # 드롭다운형식 메뉴에서 토큰 종류 선택 / 구글시트에서 토큰 데이터 추출하여 토큰값에 입력
        time.sleep(1)
        dropmenu = Select(driver.find_element_by_xpath("//*[@class='select']"))
        #토큰 가져오기
        dropmenu.select_by_value(token)
        time.sleep(1)

        #주소 입력하기
        inputadress = driver.find_element_by_xpath("//input[@name='search_word']")
        inputadress.clear()
        time.sleep(2)
        #주소 가져오기(변수) / 구글시트에서 주소 데이터 추출하여 토큰값에 입력       
        inputadress.send_keys(adress)
        time.sleep(1)

        # 구글에서 추출한 토큰 및 주소로 mdm 보내기, 클릭
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/main/div/section/div[1]/form/button").click()      
        print('{0}, {1}주소로 토큰 발행합니다.'.format(token, adress))
        time.sleep(15)

    #실패 Alert 노출 시 동작 설정하기
    # ids = 변수 id 호출하여 Alert 종류 확인 / comment = id에 따른 Alert 코멘트 출력
    def failresult(ids, comment):
        a  
        count = counta('count', a)
    
        # 노출된 Alert 체크 후 해당 Alert 출력
        text = driver.find_elements_by_xpath('//*[@id="alert-{}"]/div[1]'.format(ids))        
        for i in text:
            print(i.text)
            break
        # 노출된 Alert에 따른 코멘트 구글 시트에 입력
        sh.update_cell((count + 2), 5, comment[0])
        sh.update_cell((count + 2), 9, comment[1])
        time.sleep(2)

        #wallet 화면으로 전환        
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(60)            

        # 현재 지갑의 주소
        adressinfo = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        mdmasset = driver.find_elements_by_xpath("//*[@class='currency-display-component__text']")
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath("//*[@class='currency-display-component__suffix']")
        # 현재 주소에 따른 자산 노출 및 테스트 회차 출력
        for asset in mdmasset:
            for curren in currency:
                print('현재 {0}주소의 자산은 {1}{2} 입니다.'.format(adressinfo, asset.text, curren.text))                                        
                print('{0} {1}회차 전송 실패하였습니다.'.format(comment[2], count))
                break
        # 구글 시트에 노출된 자산 입력
        sh.update_cell((count + 2), 7, asset.text)       
        time.sleep(2)        
        print('{}초 대기 합니다.'.format(5))        
        time.sleep(5)

    #성공 Alert 노출 시 동작 설정하기
    # ids = 변수 id 호출하여 Alert 종류 확인
    def passresult(ids):
        a    
        count = counta('count', a)        
        # 노출된 Alert 확인
        id = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(ids))
        text = driver.find_elements_by_xpath('//*[@id="alert-{}"]/div[1]'.format(ids))
        # 설정한 mdmasset 값을 구글시트에 입력
        mdmasset = 50
        for i in text:             
            print(i.text)            
            print("{}MDM을 전송 하였습니다.".format(mdmasset))
            sh.update_cell((count + 2), 5, mdmasset)
            time.sleep(2)
            break

        #wallet 화면으로 전환
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(60)

        # 현재 지갑의 주소
        adressinfo = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        mdmasset = driver.find_elements_by_xpath("//*[@class='currency-display-component__text']")
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath("//*[@class='currency-display-component__suffix']")
        # 현재 주소에 따른 자산 노출 및 테스트 회차 출력
        for asset in mdmasset:
            for curren in currency:                                
                print('현재 {0}주소의 자산은 {1}{2} 입니다.'.format(adressinfo, asset.text, curren.text))                    
                sh.update_cell((count + 2), 7, asset.text)
                print('{}회차 전송 성공하였습니다.'.format(count))
                break

        time.sleep(2)
        # 구글에 전송 후 대기시간 참조하여 데이터 가져오기
        t = int(sh.cell((count + 2), 10).value)
        print('{}초 대기 합니다.'.format(t))
        time.sleep(t)

    #종료 시간
    def endtime():
        a
        count = counta('count', a)
        time.sleep(2)
        print("총 {}회 진행 완료 했습니다.".format(count))
        
        #종료시간 측정
        end = time.time()
        
        #종료시간 노출
        now = datetime.datetime.now()
        endtime = now.strftime('%H:%M:%S')
        print("전송 종료시간은 {} 입니다.".format(endtime))
        time.sleep(2)

        #종료시간 - 시작시간 계산하여 경과시간 측정
        sec = end - start
        result = str(datetime.timedelta(seconds=sec)).split(".")
        print("총 소요시간은 {} 입니다.".format(result[0]))
        time.sleep(2)