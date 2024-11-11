import pytest
from driver_setup import setup_driver
import time
from appium.webdriver.common.appiumby import AppiumBy


class TestCoordinates:
    def setup_method(self):
        self.driver = setup_driver()

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def test_get_coordinates(self):
        """화면 터치 시 좌표 출력"""
        # 화면 크기 출력
        size = self.driver.get_window_size()
        print(f"화면 크기: width={size['width']}, height={size['height']}")

        # 스크린샷 저장
        self.driver.save_screenshot('game_screen.png')

        print("30초 동안 화면을 터치하면 좌표가 출력됩니다...")
        start_time = time.time()

        while time.time() - start_time < 30:
            try:
                # 현재 화면 정보 출력
                print("\n현재 화면 정보:")
                print(f"현재 Activity: {self.driver.current_activity}")

                # 터치 이벤트 대기
                actions = self.driver.actions()
                actions.pointer_action.move_to_location(100, 100)
                actions.pointer_action.click()
                actions.perform()

                # 현재 포인터 위치 출력
                pointer_pos = actions.pointer_action.get_position()
                print(f"터치 좌표: x={pointer_pos['x']}, y={pointer_pos['y']}")

                time.sleep(1)
            except Exception as e:
                print(f"에러 발생: {str(e)}")