# DANDE
*쉽고  빠른 암호화  프로그램*

## 기능
* 파일 암호화
* 파일 복호화
* 디렉토리에 생성/수정되는 파일을 자동으로 암호화

## windows용 빌드
    dist 폴더에 있는 모든 파일이 필요
    gui.exe로 실행
    
    settings.json을 설정한 후, install.exe를 이용해서 컨텍스트 메뉴에 등록 가능 
###### settings.json을 변경해야 함! (How_To_Use.txt 참고)
###### 런타임 에러 발생시 다음 [배포판](https://www.microsoft.com/ko-kr/download/details.aspx?id=53840)을 설치해 보세요

## 사용법
암호화

    python main.py -encrypt 파일명 -key 암호화 키 -threads 동시작업 쓰레드 수
###### (암호화 키는 16글자여야 함)

* * *

복호화

    python main.py -decrypt 파일명 -key 암호화 키 -threads 동시작업 쓰레드 수
###### (암호화 키는 16글자여야 함)

## 필요한 라이브러리
- [pycryptodome](https://pypi.org/project/pycryptodome/)
- [psutil](https://pypi.org/project/psutil/)

* * *
곽준, 박민욱, 이경준 제작
