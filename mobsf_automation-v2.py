import os
import time
import requests
from secrets import MOBSF_API_KEY

MOBSF_URL = "http://localhost:8000"
APK_FILE = "test.apk"  # 실제 APK 파일 경로로 변경해야 합니다.

def upload_apk(file_path):
    url = f"{MOBSF_URL}/api/v1/upload"
    headers = {"Authorization": MOBSF_API_KEY}
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files, headers=headers)
    return response.json()

# APK 파일 업로드
response = upload_apk(APK_FILE)

if response.get("status") == "success":
    hash_value = response.get("hash")
    if hash_value:
        print("APK 파일 업로드 성공")
    else:
        print("APK 파일 업로드 응답에 해시 값이 없습니다.")
else:
    error_message = response.get("error", "알 수 없는 오류")
    print(f"APK 파일 업로드 실패: {error_message}")

# 정적 분석 실행
headers = {"Authorization": MOBSF_API_KEY}
data = {"hash": hash_value, "scan_type": "apk"}
response = requests.post(f"{MOBSF_URL}/api/v1/scan", headers=headers, data=data)

if response.status_code == 200:
    print("정적 분석 시작")
else:
    print(f"정적 분석 실행 실패: {response.json().get('error', '알 수 없는 오류')}")

# 정적 분석 완료 확인
headers = {"Authorization": MOBSF_API_KEY}
data = {"hash": hash_value}

while True:
    response = requests.post(f"{MOBSF_URL}/api/v1/report_json", headers=headers, data=data)
    if response.status_code == 200:
        report_data = response.json()
        if report_data.get("status") == "complete":
            break
        else:
            time.sleep(5)  # 5초마다 분석 완료 확인
    else:
        print(f"정적 분석 완료 확인 실패: {response.json().get('error', '알 수 없는 오류')}")
        break

# PDF 보고서 다운로드
response = requests.post(f"{MOBSF_URL}/api/v1/download_pdf", headers=headers, data=data)

if response.status_code == 200:
    with open("static_analysis_report.pdf", "wb") as f:
        f.write(response.content)
    print("정적 분석 PDF 보고서 다운로드 완료")
else:
    print(f"PDF 보고서 다운로드 실패: {response.json().get('error', '알 수 없는 오류')}")

# JSON 보고서 저장
with open("static_analysis_report.json", "w") as f:
    f.write(response.text)
print("정적 분석 JSON 보고서 저장 완료")