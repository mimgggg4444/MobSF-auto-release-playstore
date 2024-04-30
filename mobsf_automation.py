import os
import requests

from bs4 import BeautifulSoup
import time

# MOBSF 서버 URL
MOBSF_URL = 'http://localhost:8000'
# http://0.0.0.0:8000/


# 분석할 APK 파일이 있는 폴더 경로
APK_FOLDER = '/path/to/apk/folder'

# 결과 보고서 저장 폴더 경로
REPORT_FOLDER = '/path/to/report/folder'

# CSRF 토큰 가져오기
def get_csrf_token():
    response = requests.get(MOBSF_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')
    return csrf_token

# APK 파일 업로드 및 분석 요청
def upload_and_analyze(file_path, csrf_token):
    files = {'file': open(file_path, 'rb')}
    headers = {'X-CSRFToken': csrf_token}
    response = requests.post(f'{MOBSF_URL}/upload/', files=files, headers=headers)
    return response.json()

# 분석 결과 확인 및 보고서 다운로드
def check_analysis_result(analyzer_url, file_hash, file_name):
    result_url = f'{analyzer_url}/{file_hash}/'
    report_pdf_url = f'{result_url}pdf/?pdf=1'
    report_html_url = f'{result_url}html/'

    # 분석 완료 확인
    while True:
        response = requests.get(result_url)
        if 'Analysis Completed' in response.text:
            break
        time.sleep(10)  # 10초마다 확인

    # PDF 보고서 다운로드
    report_pdf = requests.get(report_pdf_url)
    with open(os.path.join(REPORT_FOLDER, f'{file_name}.pdf'), 'wb') as f:
        f.write(report_pdf.content)

    # HTML 보고서 다운로드
    report_html = requests.get(report_html_url)
    with open(os.path.join(REPORT_FOLDER, f'{file_name}.html'), 'wb') as f:
        f.write(report_html.text.encode('utf-8'))

# 메인 함수
def main():
    csrf_token = get_csrf_token()

    for file_name in os.listdir(APK_FOLDER):
        if file_name.endswith('.apk'):
            file_path = os.path.join(APK_FOLDER, file_name)
            result = upload_and_analyze(file_path, csrf_token)

            if result['status'] == 'ok':
                analyzer_url = result['analyzer']
                file_hash = result['hash']
                check_analysis_result(analyzer_url, file_hash, file_name)
            else:
                print(f"Error: {result['description']}")

if __name__ == '__main__':
    main()