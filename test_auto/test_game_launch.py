from appium import webdriver
from driver_setup import setup_driver
from config import TestConfig
import time


class TestGameLaunch:
    def setup_method(self):
        self.driver = setup_driver()

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def handle_ad(self):
        """광고 닫기 버튼 클릭"""
        print("광고 화면 처리 중...")
        try:
            # 광고 닫기 버튼 클릭 - 좌표를 리스트 안의 튜플로 전달
            self.driver.tap([(1009, 136)])
            time.sleep(5)
            print("광고 스킵 완료")
            return True
        except Exception as e:
            print(f"광고 스킵 실패: {str(e)}")
            return False

    def handle_popup(self):
        """팝업 닫기 버튼 클릭"""
        print("팝업 처리 중...")
        try:
            # 팝업 닫기 버튼 클릭 - 좌표를 리스트 안의 튜플로 전달
            self.driver.tap([(540, 1813)])
            time.sleep(5)
            print("팝업 닫기 완료")
            return True
        except Exception as e:
            print(f"팝업 닫기 실패: {str(e)}")
            return False

    def test_game_launch(self):
        """게임 실행부터 메인 화면 진입까지 테스트"""
        try:
            # 1. 게임 실행 확인
            time.sleep(25)  # 초기 로딩 대기
            current_package = self.driver.current_package
            assert current_package == TestConfig.PACKAGE_NAME, "게임이 실행되지 않았습니다"
            print("게임 실행 확인 완료")

            # 2. 광고 처리
            assert self.handle_ad(), "광고 처리 실패"

            # 3. 팝업 처리
            assert self.handle_popup(), "팝업 처리 실패"

            print("모든 과정 완료 - 메인 화면 진입 성공!")

        except Exception as e:
            # 실패 시 스크린샷 저장
            self.driver.save_screenshot('error_screen.png')
            raise e