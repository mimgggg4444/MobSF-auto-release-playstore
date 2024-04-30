import requests
from secrets import MOBSF_API_KEY


# MOBSF 서버 URL
MOBSF_URL = "http://localhost:8000"

# MOBSF API 키
API_KEY = MOBSF_API_KEY

# APK 파일 경로
# 파일위치 업데이트
APK_FILE = "path/to/apk/"

# 1. APK 파일 업로드
with open(APK_FILE, "rb") as f:
    files = {"file": f}
    headers = {"Authorization": API_KEY}
    response = requests.post(f"{MOBSF_URL}/api/v1/upload", headers=headers, files=files)

if response.status_code == 200:
    data = response.json()
    hash_value = data["hash"]
    print(f"APK 파일 업로드 완료. 해시 값: {hash_value}")
else:
    print(f"APK 파일 업로드 실패: {response.json()['error']}")

# 2. 정적 분석 실행
headers = {"Authorization": API_KEY}
data = {"hash": hash_value}
response = requests.post(f"{MOBSF_URL}/api/v1/scan", headers=headers, data=data)

if response.status_code == 200:
    print("정적 분석 시작")
else:
    print(f"정적 분석 실패: {response.json()['error']}")

# 3. 정적 분석 완료 확인 및 보고서 다운로드
headers = {"Authorization": API_KEY}
data = {"hash": hash_value}

while True:
    response = requests.post(f"{MOBSF_URL}/api/v1/scan", headers=headers, data=data)
    if "Analysis Completed" in response.text:
        break

# PDF 보고서 다운로드
response = requests.post(f"{MOBSF_URL}/api/v1/download_pdf", headers=headers, data=data)
with open("static_analysis_report.pdf", "wb") as f:
    f.write(response.content)
print("정적 분석 PDF 보고서 다운로드 완료")

# JSON 보고서 다운로드
response = requests.post(f"{MOBSF_URL}/api/v1/report_json", headers=headers, data=data)
with open("static_analysis_report.json", "w") as f:
    f.write(response.text)
print("정적 분석 JSON 보고서 다운로드 완료")