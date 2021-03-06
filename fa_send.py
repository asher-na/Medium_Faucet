#-*- coding: utf-8 -*- 
import time
import datetime
import fa_func
import warnings
import gspread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#구글 스프레드 시트 위치: https://docs.google.com/spreadsheets/d/1NVGssWH9tl_X7HW2Rwpff8M4INiTSQSfSvGayinUD6E/edit#gid=0
gs = gspread.service_account(filename="../google/sheetkey.json") #참조할 구글시트에 공유 되어있는 json 파일 추가
sh = gs.open("Faucet_auto").worksheet("faucet_send")
sh1 = gs.open("Faucet_auto").worksheet("Summary")

driver = fa_func.driver
id = fa_func.id
count = 0
# 구글시트 B영역에 입력된 데이터 갯수 계산 후 Count에 대입
test_count = action_count = sh.col_values(2)

#경고 무시
warnings.filterwarnings('ignore')

# 지갑 및 faucet 화면 가져오기
fa_func.wallet.extention()

# 기존에 생성한 계정(주소)을 seed 구문으로 가져오기
fa_func.wallet.importwallet()

# 네트워크 변수 적용하여 지갑 네트워크 세팅하기 (mdl, besu 네트워크)
fa_func.wallet.settingnet()

# 시작시간 측정하기
fa_func.faucet.starttime()

# 구글시트 참고하여 n 회 실행 / 구글시트 행에 count 증가 값을 줘서 위에서부터 차례대로 실행하게 설정
while count <(len(test_count)-2):
    # 함수 내부 count 증가를 위한 조건 추가       
    count = count + 1
    a = count
    b = count + fa_func.counta('count', a)

    print("===={}회차 전송시작====".format(count))
    # 구글 시트 목적 부분을 참고하여 change_token, change_all 일 경우 지갑에서 네트워크 변경
    fa_func.faucet.changenet()

    # 구글 시트 목적 부분을 참고하여 change_adress, change_all 일 경우 지갑에서 계정(주소) 변경
    fa_func.faucet.changewallet()

    # 현재 설정된 지갑의 토큰 및 주소에 따른 자산 노출
    fa_func.faucet.assetprint()

    # 구글시트에서 가져온 토큰 및 주소 정보를 이용해 faucet에서 해당 토큰 및 주소로 mdm 전송
    fa_func.faucet.faucetsetting()

    # faucet에서 mdm 전송시 발생된 alert이 id[0] = red 이다
    alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[0]))
    time.sleep(2)
    ## red alert이 화면에 노출될 경우
    if alertid.is_displayed(): # Display:none인 상태를 확인하는 조건문
        # faucet 화면에 노출되는 alert 출력 / 매개변수에 입력한 comment를 출력시키거나 구글 시트에 입력
        # 지갑 화면으로 전환 후 자산 노출 및 구글 시트에 저장
        fa_func.faucet.failresult(id[0], ['주소 입력 오류로 인해'])    
    else:        
        # faucet에서 mdm 전송시 발생된 alert이 blue 인 경우        
        alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[1]))        
        time.sleep(2)
        if alertid.is_displayed():
            fa_func.faucet.failresult(id[1], ['대기시간 이내에 전송하여'])        
        else:
            # faucet에서 mdm 전송시 발생된 alert이 blue-leak 인 경우            
            alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[2]))        
            time.sleep(2)
            if alertid.is_displayed():
                fa_func.faucet.failresult(id[2], ['Faucet 지갑에 자산이 부족하여'])
            else:
                # faucet에서 mdm 전송시 발생된 alert이 red-etc 인 경우                
                alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[3]))        
                time.sleep(2)
                if alertid.is_displayed():
                    fa_func.faucet.failresult(id[3], ['오류 발생하여'])
                else:
                    # faucet에서 mdm 전송시 발생된 alert이 green 인 경우
                    try:
                        WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="alert-{}"]/div[1]'.format(id[4]))))
                    except:
                        fa_func.faucet.alertError()
                    else:
                        # faucet 화면에 노출되는 alert 출력 / 지갑 화면으로 전환 후 자산 노출 및 구글 시트에 저장                    
                        alertid = driver.find_element_by_xpath('//*[@id="alert-{}"]'.format(id[4]))        
                        if alertid.is_displayed():
                            fa_func.faucet.passresult(id[4])
                        

    if count ==(len(test_count)-2):
        # while문 종료시 종료 시간 노출 및 총 소요시간 측정
        fa_func.faucet.endtime()
        time.sleep(2)
        fa_func.faucet.get_print()
        break

# 구글 시트에 결과 정리
fa_func.sh1.append_row([str(datetime.datetime.now()),str(fa_func.g_estimate),str(fa_func.sh.acell('K2').value), str(fa_func.g_sheet_reason)])