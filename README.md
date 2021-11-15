Faucet test
======================
Faucet을 통해 테스트넷에 토큰을 전송하는 자동화 케이스 구현
> Medium wallet에서 실전 연습을 하기위한 토큰 제공 수단으로, MDM 토큰을 Medium wallet의 다양한 네트워크 및 주소로 전송할 수 있다.

## install
* #### [Chrome Webdriver](https://chromedriver.chromium.org/, "chromewebdriver link")
* #### [Medium wallet](https://chrome.google.com/webstore/detail/medium-wallet/olkbchllhcflpbjfgagahpkjnjioiedg?hl=ko, "mediumwallet link")
* #### [Chrome extension source viewer](https://chrome.google.com/webstore/detail/chrome-extension-source-v/jifpbeccnghkjeaalbbjmodiffmgedin, "chrome extension source link")
* #### [selenium으로 크롬 확장 도구 사용하기 링크 (참조)](https://otrodevym.tistory.com/entry/selenium-selenium%EC%9C%BC%EB%A1%9C-%ED%81%AC%EB%A1%AC-%ED%99%95%EC%9E%A5-%EB%8F%84%EA%B5%AC-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0, "link")
  

## google sheet
* #### [Google spread sheet link](https://docs.google.com/spreadsheets/d/1NVGssWH9tl_X7HW2Rwpff8M4INiTSQSfSvGayinUD6E/edit#gid=0, "google link")
#### * json을 통해 구글시트와 공유 (sheetkey.json)
	
	[참조영역] - 원하는 데이터로 변경
	목적 : normal, change_token, change_adress, change_all
		normal : 토큰, 주소 변경 없는 케이스
		change_token : 토큰 변경 케이스
		change_adress : 주소 변경 케이스
		change_all : 토큰, 주소 변경 케이스
		* 주소 오입력 케이스는 change_adress, change_all 외 항목 선택
	토큰 : besu, mdl, erc20 제공
	주소 : 이미 생성해 놓은 계정의 주소 (구글시트 하단 참조)
	전송 후 대기시간 : 다음 행 진행 시 영향을 줌 / 동일 토큰, 주소는 1시간에 1회씩 50mdm 제공하여 3600을 입력해야 전송 가능

## Data setting
	fa_func.py
	1. faucet URL, password, network, token 등 추가 및 변경되는 사항들에 대해 수정
	
## Excution
	while count 값을 변경해 반복횟수 조정
	> python fa_send.py	

## Features
* ### 지갑 정보 노출
  + 구글시트에서 가져온 네트워크 및 주소를 wallet에 설정 후 해당 wallet의 정보(자산)을 출력
     - 현재 정보(자산) 출력 및 구글시트에 입력
```
토큰 변경 케이스 (change_token, change_all)
fa_func.faucet.changenet() 실행되어 wallet에서 네트워크 변경케이스 추가

주소 변경 케이스 (change_adress, change_all)
fa_func.faucet.changewallet() 실행되어 wallet에서 계정 변경케이스 추가
```
* ### 토큰 전송
  + Faucet에서 위에 설정한 네트워크에 해당하는 토큰을 동일한 주소로 전송
     - 전송한 토큰수량 출력 및 구글시트에 입력
     - 예외사항(주소 오입력, 대기시간 미만 전송 등)발생시 위와 동일

* ### 토큰 수신 확인
  + 지갑 화면으로 전환 후 Faucet을 통해 수신한 토큰 확인
     - 토큰 수신 후 현재 정보(자산) 출력 및 구글시트에 입력
