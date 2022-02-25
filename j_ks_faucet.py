from curses import meta
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import gspread
import random
import platform
import pyperclip
import warnings

warnings.filterwarnings('ignore')

sysOS = platform.system()
options = webdriver.ChromeOptions()
if (sysOS == 'Windows'):
    _chromedriver = '../driver/window_chromedriver' #chromedriver 위치에 따라 변경해야 함
    print('Windows')
else:
    _chromedriver = '/Users/medium/autotest/selenium/driver/chromedriver' #chromedriver 위치에 따라 변경해야 함    
    print('MacOS')
packed_extension_path = '/Users/medium/autotest/selenium/crx/Metamask.crx' #chrome extension 위치에 따라 변경해야 함
options.add_extension(packed_extension_path)
driver = webdriver.Chrome(_chromedriver, options=options)

#=======================공통 변수============================
#구글 스프레드 시트 위치: https://docs.google.com/spreadsheets/d/1NVGssWH9tl_X7HW2Rwpff8M4INiTSQSfSvGayinUD6E/edit#gid=0
gs = gspread.service_account(filename="/Users/medium/autotest/selenium/google/sheetkey.json") #참조할 구글시트에 공유 되어있는 json 파일 추가
sh = gs.open("ks_faucet_auto").worksheet("faucet_send")
sh1 = gs.open("ks_faucet_auto").worksheet("Summary")

#Test를 위해 생성해놓은 계정 주소와 그에따른 Seed 구문
#wallet 계정 변경 시 구글 시트에서 주소를 참조해 아래 주소와 비교하여 seed 구문을 가져오도록 되어 있음
address_seed = {"0x1914627a35cf0822714f79D2584b278F92fC8be5":"bind orbit account repeat buddy sad clog property vapor cake raven original",
            "0xF6ef8923316B3D12C8fb537EFd486059427a1c7D":"tower boost ready buddy task sudden lake lemon charge hamster capital organ",
            "0x4c7eD9DA6b7f123b70E55519020268B03C9247D7":"mixed distance resemble valve saddle message post pledge acid nurse spider absorb",
            "0xcBe046c536AC02A12123017269f0D2439CdD0774":"heart endorse abstract caught cave edit rebel rain steak organ lyrics stomach",
            "0x81b3E378eDEeA4C1D9fBaC70F0148755B74Ac16a":"fantasy dune decorate stuff fetch poet tornado place gown gasp gesture motion",
            "0xeE057c636d3822B949Ed3BAA59E683F69206435b":"review ceiling fresh yellow guard vicious pole match bronze claw spawn measure",
            "0xDFf052e718Da3F031be03BDC96133A0289F0C115":"mean demise deny exotic average stumble list silly visa floor wisdom equal",
            "0x5c6cF77f0Aa6653b1f3c18ee898AcD8feB7Cb8a5":"laundry spirit defense doll fall rhythm solution more profit retreat cattle vibrant",
            "0x97a43358AB8D71359149Dc4296c4E22e804Dc0d5":"scatter lion acoustic error able pill service spot budget pattern absent father",
            "0xA218471bB241A55506E471bD041716ca87E50f30":"knife matrix waste begin abstract tennis bundle off edge credit fade draft"}

#=======================Faucet 변수============================
#Faucet 주소
url = 'https://faucet.stage.kstadium.io/'

#Faucet 전송시 Alert 종류
id = ['red', 'blue', 'blue-leak', 'red-etc', 'green']

#=======================Wallet 변수============================
#지갑 비밀번호
password = 'vnfmsgk12#'
token_addr_dict = '0x24d6517616D770DD9FaE8A7C23C4113988eF5895'
excel_E = 'E'
excel_F = 'F'
#============================================================================================================================================
#               Wallet 설정 
#============================================================================================================================================

class Wallet:    

    # # webdriver 재 실행을 위함
    # def drivers():
    #     global driver
    #     options = webdriver.ChromeOptions()
    #     if (sysOS == 'Windows'):
    #         _chromedriver = '../driver/window_chromedriver' #chromedriver 위치에 따라 변경해야 함
    #         print('Windows')
    #     else:
    #         _chromedriver = '../driver/chromedriver' #chromedriver 위치에 따라 변경해야 함    
    #         print('MacOS')
    #     packed_extension_path = '../crx/Metamask.crx' #chrome extension 위치에 따라 변경해야 함
    #     options.add_extension(packed_extension_path)
    #     driver = webdriver.Chrome(_chromedriver, options=options)

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

    def createwallet():
        #metamask wallet 설정
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/button').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/div[4]/div[1]/div/input').send_keys(address_seed["0x1914627a35cf0822714f79D2584b278F92fC8be5"])
        driver.find_element_by_xpath('//*[@id="password"]').send_keys('vnfmsgk12#')
        driver.find_element_by_xpath('//*[@id="confirm-password"]').send_keys('vnfmsgk12#')
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/div[7]/div').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/form/button').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[2]/div/div/button').click()
        time.sleep(3)
        #driver.find_element_by_xpath('//*[@id="popover-content"]/div/div/section/header/div/button').click()
        time.sleep(3)
    
    def change_net():
        #wallet net 변경
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
        action = ActionChains(driver)
        submenu = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(text(), "{}")]'.format('Ropsten 테스트 네트워크'))))
        action.move_to_element(submenu).click().perform()
        time.sleep(4)

    def import_token():
        time.sleep(2)
        driver.find_element_by_link_text("Import tokens").click()
        time.sleep(2)
        # 토큰 주소 입력
        driver.find_element_by_xpath("//input[@id='custom-address']").send_keys(token_addr_dict)
        time.sleep(2)
        # Import tokens
        driver.find_element_by_xpath("//button[@class='button btn--rounded btn-primary page-container__footer-button']").click()
        time.sleep(2)
        driver.find_element_by_xpath("//button[@class='button btn--rounded btn-primary btn--large page-container__footer-button']").click()
        time.sleep(2)
        # 창 닫기
        driver.find_element_by_css_selector("i[data-testid='asset__back']").click()

        #wallet에서 자산 노출하기


class Faucet:

    def result(id):    
        # 노출된 Alert 체크 후 해당 Alert 출력        
        text = driver.find_elements_by_xpath('//*[@id="alert-{}"]/div[1]'.format(id))        
        for i in text:
            result_text = i.text
            break     
        return result_text
    
    def change_wallet(start):        
        address = sh.acell('B' + str(start)).value
        #Account menu 진입하여 잠금 버튼 클릭 
        time.sleep(2)
        driver.find_element_by_xpath("//*[@class='identicon__address-wrapper']").click()
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div[2]/button').click()

        # 계정을 복구하시겠습니까 버튼 클릭
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div[3]/span/button').click()

        #시드 구문 입력하기
        time.sleep(2)
        seedinput = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[4]/div[1]/div/input')
        #adress_seed에 입력된 주소를 가져와서 그에따른 seed 구문 호출
        seedinput.send_keys(address_seed[address])

        #암호 입력
        time.sleep(2)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(2)
        #password 값에 입력한 데이터 가져오기
        driver.find_element_by_id('confirm-password').send_keys(password)

        #복구 버튼 활성화 확인
        nextBtn = driver.find_element_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/button')                
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
        #metamask 로고 클릭하여 홈화면 노출
        driver.find_element_by_xpath('//*[@id="app-content"]/div/div[1]/div/div[1]/img[1]').click()

        time.sleep(3)
        # 현재 지갑의 주소
        address_info = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        kok_asset = driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[2]/button/h2/span[1]')
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[2]/button/h2/span[2]')
        # 현재 주소에 따른 자산 노출 및 테스트 회차 출력
        for asset in kok_asset:
            for curren in currency:
                print(asset.text + curren.text)              
                break


    def input_address(start):
        address = sh.acell('B' + str(start)).value
        driver.switch_to.window(driver.window_handles[-1])
        #주소 입력하기
        time.sleep(2)
        inputadress = driver.find_element_by_xpath("//input[@name='search_word']")
        inputadress.clear()
        time.sleep(2)
        #주소 가져오기(변수) / 구글시트에서 주소 데이터 추출하여 토큰값에 입력       
        inputadress.send_keys(address)        
        time.sleep(2)

    def send_kok(start):
        # 구글에서 추출한 토큰 및 주소로 mdm 보내기, 클릭
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="btn-send"]').click()              
        time.sleep(2)
        
        # faucet에서 로딩화면이 2분 이상 지속되면 실패로 간주
        loading_time = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20]
        for i in loading_time:                
            loading_btn = driver.find_element_by_xpath('//*[@id="loading-btn"]')
            if loading_btn.is_displayed():        
                time.sleep(i)

            else:
                # faucet에서 mdm 전송시 발생된 alert이 id[0] = red 이다
                alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[0]))
                time.sleep(2)
                # red alert이 화면에 노출될 경우
                if alertid.is_displayed(): # Display:none인 상태를 확인하는 조건문
                    # faucet 화면에 노출되는 alert 출력 / 매개변수에 입력한 comment를 출력시키거나 구글 시트에 입력
                    # 지갑 화면으로 전환 후 자산 노출 및 구글 시트에 저장
                    Faucet.result(id[0])    
                    print(Faucet.result(id[0]))
                    sh.update_acell('D' + str(start), Faucet.result(id[0]))                 

                else:        
                    # faucet에서 mdm 전송시 발생된 alert이 blue 인 경우        
                    alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[1]))        
                    time.sleep(2)
                    if alertid.is_displayed():
                        Faucet.result(id[1])    
                        print(Faucet.result(id[1]))    
                        sh.update_acell('D' + str(start), Faucet.result(id[1]))    
                    else:
                        # faucet에서 mdm 전송시 발생된 alert이 blue-leak 인 경우            
                        alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[2]))        
                        time.sleep(2)
                        if alertid.is_displayed():
                            Faucet.result(id[2])
                            print(Faucet.result(id[2]))
                            sh.update_acell('D' + str(start), Faucet.result(id[2]))    
                        else:
                            # faucet에서 mdm 전송시 발생된 alert이 red-etc 인 경우                
                            alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[3]))        
                            time.sleep(2)
                            if alertid.is_displayed():
                                Faucet.result(id[3])
                                print(Faucet.result(id[3]))
                                sh.update_acell('D' + str(start), Faucet.result(id[3]))    
                            else:
                                alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[4]))        
                                if alertid.is_displayed():
                                    Faucet.result(id[4])
                                    print(Faucet.result(id[4]))     
                                    sh.update_acell('D' + str(start), Faucet.result(id[4]))    

                time.sleep(2)                   
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(60)
                break

            if i == 20:
                print("로딩 지속 노출로 인해 확인 불가합니다.")  
                sh.update_acell('D' + str(start), "로딩 지속 노출로 인해 확인 불가합니다.")    
                time.sleep(2)

                #wallet 화면으로 전환        
                driver.switch_to.window(driver.window_handles[0])                
                
                break  
    
    def wallet_check(start, text):
        #wallet 화면으로 전환        
        time.sleep(2)            

        # 현재 지갑의 주소
        address_info = driver.find_element_by_xpath("//*[@class='selected-account__address']")
        # 현재 자산의 양
        kok_asset = driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[2]/button/h2/span[1]')
        # 현재 자산의 통화
        currency = driver.find_elements_by_xpath('//*[@id="app-content"]/div/div[3]/div/div/div/div[3]/div/div[2]/div/div[2]/button/h2/span[2]')
        # 현재 주소에 따른 자산 노출 및 테스트 회차 출력
        for asset in kok_asset:
            for curren in currency:
                print(asset.text + curren.text)  
                sh.update_acell(text + str(start), asset.text)                 
                break

    def wait_time(start):
        # 구글에 전송 후 대기시간 참조하여 데이터 가져오기
        t = int(sh.acell('I' + str(start)).value)
        print('{}초 대기 합니다.'.format(t))
        time.sleep(t)

    def endtime():
        global g_estimate
                
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
        g_estimate = result[0]
        time.sleep(2)

    def get_print():
        global g_sheet_reason
        result_count = sh.col_values(7)
        Pass = 'Pass'
        NPass = 'NPass'
        Fail = 'Fail'
        Total_count = [i for i in range(len(result_count)-2)]
        Pass_count = [i for i in range(len(result_count)) if Pass in result_count[i]]
        NPass_count = [i for i in range(len(result_count)) if NPass in result_count[i]]
        Fail_count = [i for i in range(len(result_count)) if Fail in result_count[i]]
        print('=======================================================================')
        print('============================Test end====================================')
        print('=======================================================================')
        print('Total : {0} | Pass : {1} | NPass : {2} | Fail : {3}'.format(len(Total_count), len(Pass_count),len(NPass_count), len(Fail_count)))
        print('============================Fail reason================================')
        reason = sh.range('H3:H100')
        g_sheet_reason = ""
        for cell in reason:    
            if "Faucet" in cell.value:    
                g_sheet_reason = g_sheet_reason + cell.value
                reason_value = cell.value                    
                print(reason_value)
        
    

#구글 스프레드 시트의 기존 데이터 삭제
sh.batch_clear(["D3:D100", "E3:E100", "F3:F100"])

Wallet.extention()
Wallet.createwallet()
Wallet.change_net()
Wallet.import_token()

for start in range(3, 16):
    if sh.acell('A' + str(start)).value == "change_address":
        Faucet.change_wallet(start)   
        Wallet.import_token()     
    else:
        pass
    Faucet.wallet_check(start, excel_E)
    Faucet.input_address(start)
    Faucet.send_kok(start)
    Faucet.wallet_check(start, excel_F)
    Faucet.wait_time(start)
    
Faucet.get_print()

# 구글 시트에 결과 정리
sh1.append_row([str(datetime.datetime.now()),str(sh.acell('J2').value), str(g_sheet_reason)])
driver.quit()