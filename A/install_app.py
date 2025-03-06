from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import yaml

# appium_config.yaml 파일에서 설정 로드 예시
with open("appium_config.yaml", "r") as f:
    config = yaml.safe_load(f)

desired_caps = config['desired_capabilities']
appium_server = config['appium_server']  # 예: http://localhost:4723/wd/hub

driver = webdriver.Remote(appium_server, desired_caps)

def install_app(package_name):
    # Play Store 앱이 실행되어 있다고 가정하고,
    # 검색창 클릭 및 검색어 입력
    search_box = driver.find_element(By.ID, "com.android.vending:id/search_box_idle_text")
    search_box.click()
    
    search_input = driver.find_element(By.CLASS_NAME, "android.widget.EditText")
    search_input.send_keys(package_name)
    search_input.send_keys(Keys.ENTER)
    
    time.sleep(3)  # 검색 결과 대기
    
    # 설치 버튼 클릭 (버튼 텍스트가 '설치'인 버튼)
    install_button = driver.find_element(By.XPATH, "//android.widget.Button[contains(@text, '설치')]")
    install_button.click()
    
    # 설치 완료 대기 (단순 sleep, 실제로는 설치 완료 이벤트를 감지할 수 있음)
    time.sleep(30)
    print(f"{package_name} 설치 완료.")

if __name__ == "__main__":
    target_package = "com.example.app"  # 예시 패키지명
    install_app(target_package)
    driver.quit()
