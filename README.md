Encrypt_My_FIles
===

## 16비트를 한 블록으로 처리해서, 1블록은 평문, 1블록은 암호화를 반복함

## 사용법
암호화

    python main.py -encrypt 파일명 -key 암호화 키 -threads 동시작업 쓰레드 수
###### (암호화 키는 16글자여야 함)

* * *

복호화

    python main.py -decrypt 파일명 -key 암호화 키 -threads 동시작업 쓰레드 수
###### (암호화 키는 16글자여야 함)

## windows용 빌드
    dist 폴더에 있는 모든 파일이 필요
    gui.exe로 실행
###### settings.json을 변경해야 함! (How_To_Use.txt 참고)

## 필요한 라이브러리
- [pycryptodome](https://pypi.org/project/pycryptodome/)
- [psutil](https://pypi.org/project/psutil/)
