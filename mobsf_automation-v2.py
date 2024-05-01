import os
import time
import requests

MOBSF_URL = "http://localhost:8000"
APK_FILE = "test.apk"

# api key는 변경됩니다.
MOBSF_API_KEY = "20a58cbecc25de86319138e927ff7f67c98d000e96a627921f09c5eae1322d29"

def upload_apk(file_path):
    url = f"{MOBSF_URL}/api/v1/upload"
    headers = {"Authorization": MOBSF_API_KEY}
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files, headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        return {"status": "success", "hash": response_data.get("hash")}
    else:
        return {"status": "error", "error": response_data.get("error", "Unknown error")}

# APK 파일 업로드
response = upload_apk(APK_FILE)
if response.get("status") == "success":
    hash_value = response.get("hash")
    if hash_value:
        print("APK 파일 업로드 성공")
        print(f"해시 값: {hash_value}")
        
        # 정적 분석 실행
        headers = {"Authorization": MOBSF_API_KEY}
        data = {"hash": hash_value, "scan_type": "apk"}
        response = requests.post(f"{MOBSF_URL}/api/v1/scan", headers=headers, data=data)
        if response.status_code == 200:
            print("정적 분석 시작")
        else:
            print(f"정적 분석 실행 실패: {response.json().get('error', '알 수 없는 오류')}")
        
# 정적 분석 완료 확인
        while True:
            response = requests.post(f"{MOBSF_URL}/api/v1/scan", headers=headers, data={"hash": hash_value})
            if response.status_code == 200:
                if response.json().get("status") == "completed":
                    print("정적 분석 완료")
                    break
                else:
                    time.sleep(5)  # 5초 간격으로 분석 완료 여부 확인
            else:
                print(f"정적 분석 상태 확인 실패: {response.json().get('error', '알 수 없는 오류')}")
                break
        
        # PDF 보고서 다운로드
        response = requests.post(f"{MOBSF_URL}/api/v1/download_pdf", headers=headers, data={"hash": hash_value})
        if response.status_code == 200:
            with open("static_analysis_report.pdf", "wb") as f:
                f.write(response.content)
            print("정적 분석 PDF 보고서 다운로드 완료")
        else:
            print(f"PDF 보고서 다운로드 실패: {response.json().get('error', '알 수 없는 오류')}")
        
        # JSON 보고서 저장
        response = requests.post(f"{MOBSF_URL}/api/v1/report_json", headers=headers, data={"hash": hash_value})
        if response.status_code == 200:
            with open("static_analysis_report.json", "w") as f:
                f.write(response.text)
            print("정적 분석 JSON 보고서 저장 완료")
        else:
            print(f"JSON 보고서 저장 실패: {response.json().get('error', '알 수 없는 오류')}")
        
    else:
        print("APK 파일 업로드 응답에 해시 값이 없습니다.")
else:
    error_message = response.get("error", "알 수 없는 오류")
    print(f"APK 파일 업로드 실패: {error_message}")