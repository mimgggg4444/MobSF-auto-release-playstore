import os
import time
import requests
import logging


# 8000 port 사용
MOBSF_URL = "http://localhost:8000"
APK_FILE = "/Users/e/Desktop/test.apk"

# api key는 변경됩니다.
MOBSF_API_KEY = "19f83e6d4402854fb0148c3a00acf7decd543552f846363e4e7bee19824b643f"

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_apk(file_path):

    if not os.path.isfile(file_path):
        logger.error(f"파일을 찾을 수 없습니다: {file_path}")
        return {"status": "error", "error": f"File not found: {file_path}"}


    url = f"{MOBSF_URL}/api/v1/upload"
    headers = {"X-Mobsf-Api-Key": MOBSF_API_KEY}

    # 파일 문제 파일 경로 및 files 제대로 설정. 이유 요청
    # files = {"file": open(file_path, "rb")}
    files = {"file": ("test.apk", open(file_path, "rb"), "application/vnd.android.package-archive")}


    # 추가 코드
    try:
        response = requests.post(url, files=files, headers=headers)
        response.raise_for_status()  # 오류 발생 시 예외 발생
        
        logger.info(f"응답 상태 코드: {response.status_code}")
        logger.info(f"응답 내용: {response.text}")
        
        response_data = response.json()
        return {"status": "success", "hash": response_data.get("hash")}

    except requests.exceptions.RequestException as e:
        logger.error(f"APK 파일 업로드 중 오류 발생: {e}")
        return {"status": "error", "error": str(e)}




# APK 파일 업로드
response = upload_apk(APK_FILE)
if response.get("status") == "success":
    hash_value = response.get("hash")
    if hash_value:
        logger.info("APK 파일 업로드 성공")
        logger.info(f"해시 값: {hash_value}")

        
        # 정적 분석 실행
        headers = {"X-Mobsf-Api-Key": MOBSF_API_KEY}
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
        logger.warning("APK 파일 업로드 응답에 해시 값이 없습니다.")
else:
    error_message = response.get("error", "알 수 없는 오류")
    logger.error(f"APK 파일 업로드 실패: {error_message}")
