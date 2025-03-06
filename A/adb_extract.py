import subprocess
import os

def extract_apk(package_name, local_storage_path):
    # adb 명령어로 패키지 위치를 찾고, APK 파일 경로 확인
    try:
        result = subprocess.check_output(["adb", "shell", "pm", "path", package_name])
        result = result.decode("utf-8").strip()
        # 결과 예시: package:/data/app/com.example.app-1/base.apk
        apk_path = result.split(":", 1)[1]
        print(f"APK 경로: {apk_path}")
    except Exception as e:
        print("APK 경로 확인 실패:", e)
        return

    # 로컬 저장 경로에 파일 추출
    local_apk_file = os.path.join(local_storage_path, f"{package_name}.apk")
    try:
        subprocess.check_call(["adb", "pull", apk_path, local_apk_file])
        print(f"APK 추출 완료: {local_apk_file}")
    except Exception as e:
        print("APK 추출 실패:", e)

if __name__ == "__main__":
    package = "com.example.app"
    local_path = "./apk_storage"  # Appium PC의 로컬 저장소
    os.makedirs(local_path, exist_ok=True)
    extract_apk(package, local_path)
