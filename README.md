


### mobsf


```
여러 대의 디바이스를 준비하고, UI 자동화 도구(Appium)로 앱 다운로드 자동화.
ADB를 사용하여 APK를 추출 후 서버로 전송.
서버에서 MobSF를 이용해 자동 분석 후 취약한 앱 탐색.
```



폴더를 선택
안에 있는 apk파일 전부 mobsf에 업로드.
플레이스토어에 등록될 수 있는 확률 퍼센트지로 나오게.
혹은 몇가지 조건이 충족되면 등록, 혹은 등록 안되게.
등록안될 경우 조건이 충족되지 않은 부분과 보완할 부분 작성될 수 있게.


```


                                  ┌────────────────────────────┐
                                  │     Google Play Store      │
                                  │  (앱 설치 원본, APK 제공)     │
                                  └─────────────▲──────────────┘
                                                │
                                     (앱 설치를 위한 명령 전달)
                                                │
                                                ▼
                  ┌────────────────────────────────────────────────┐
                  │         Agent Device (스마트폰)                │
                  │  - Appium을 이용한 Play Store 자동 제어         │
                  │  - 앱 설치 완료 후, adb 명령어로 APK 추출         │
                  │  - 추출된 APK 파일은 로컬에 저장됨                │
                  └───────────────┬────────────────────────────────┘
                                  │  (WiFi LAN)
                                  ▼
                  ┌────────────────────────────────────────────────┐
                  │         메인 리눅스 서버 (중앙 관리 서버)         │
                  │  - SCP/HTTP API를 통해 APK 수신 및 저장           │
                  │  - MobSF API 호출로 APK 자동 분석                │
                  │  - 분석 결과를 DB에 저장 (자동 저장 로직 포함)      │
                  └───────────────┬────────────────────────────────┘
                                  │
                                  ▼
                  ┌────────────────────────────────────────────────┐
                  │       스토리지 서버 (NAS/클라우드, 선택사항)       │
                  │  - 장기 보관용 APK 및 분석 결과 저장              │
                  └────────────────────────────────────────────────┘





```




핵심 흐름

Agent Device (스마트폰)

PC에서 Appium 스크립트를 이용하여 Play Store에서 앱을 자동 설치
설치 완료 후, adb를 통해 APK를 추출
추출된 APK는 SCP 프로토콜(또는 HTTP API)로 메인 리눅스 서버에 전송
전송 후, 로컬 저장소의 APK 파일은 삭제(용량 관리)
메인 리눅스 서버

전송받은 APK 파일을 지정 폴더(예: /home/user/apk_storage/)에 저장
저장된 APK에 대해 MobSF API를 호출하여 자동 분석
분석 결과는 JSON 형식으로 받아 DB에 저장 (또는 파일로 보관 후 DB에 메타데이터 저장)





-----



### 파일 구성도
## A. Appium을 이용하는 PC (Agent 컨트롤 및 APK 추출/전송)
```
appium_project/
├── requirements.txt           # Appium, paramiko, scp, 기타 라이브러리
├── appium_config.yaml         # Appium 서버 및 디바이스 설정 파일
├── install_app.py             # Appium을 사용한 Play Store 자동 설치 스크립트
├── adb_extract.py             # 설치 완료 후 APK 추출 스크립트 (adb 명령어 활용)
├── scp_transfer.py            # 추출된 APK를 메인 리눅스 서버로 전송하는 스크립트 (paramiko + scp)
└── utils/
    └── helper.py             # 공통 헬퍼 함수 (예: 로깅, 파일 체크 등)
```





## B. 메인 리눅스 서버 (APK 저장, MobSF 분석, DB 저장)
```
linux_server/
├── requirements.txt           # requests, SQLAlchemy, 기타 필요 라이브러리
├── mobsf_integration.py       # MobSF API 호출 및 분석 결과 처리 스크립트
├── db/
│   └── db_setup.py            # DB 연결, 테이블 생성 및 결과 저장 코드
├── apk_storage/               # Agent로부터 전송받은 APK 파일 저장 디렉토리
├── results/                   # MobSF 분석 결과(JSON) 저장 디렉토리
└── scheduler.py               # 전체 작업 스케줄링 및 중복 관리 (옵션)
```





- 전 기록
### mobsf를 활용한

```
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```


