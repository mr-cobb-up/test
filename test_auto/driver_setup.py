from appium import webdriver
from appium.options.android import UiAutomator2Options
import time


def setup_driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'RFCW50ZYKHZ'
    options.app_package = 'io.supercent.pizzaidle'
    options.app_activity = 'com.unity3d.player.UnityPlayerActivity'
    options.automation_name = 'UiAutomator2'
    options.no_reset = True

    try:
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=options)

        # 앱 실행
        driver.activate_app('io.supercent.pizzaidle')
        time.sleep(5)  # 앱 실행 대기

        return driver
    except Exception as e:
        print(f"드라이버 설정 실패: {str(e)}")
        raise e