from appium import webdriver
from driver_setup import setup_driver
from config import TestConfig
import time


class TestInAppPurchase:
    def setup_method(self):
        self.driver = setup_driver()

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def enter_shop(self):
        """상점 진입"""
        print("상점 진입 중...")
        try:
            # 상점 버튼 클릭
            self.driver.tap([(1000, 411)])
            time.sleep(4)
            print("상점 진입 완료")
            return True
        except Exception as e:
            print(f"상점 진입 실패: {str(e)}")
            return False

    def scroll_down(self):
        """화면 아래로 스크롤"""
        try:
            # 화면 크기 구하기
            window_size = self.driver.get_window_size()
            width = window_size['width']
            height = window_size['height']

            # 스크롤 동작 (아래로)
            start_x = width * 0.5
            start_y = height * 0.7
            end_x = width * 0.5
            end_y = height * 0.3

            self.driver.swipe(start_x, start_y, end_x, end_y, 1000)
            time.sleep(3)  # 스크롤 애니메이션 대기
            print("스크롤 완료")
            return True
        except Exception as e:
            print(f"스크롤 실패: {str(e)}")
            return False

    def click_purchase_button_with_option(self, purchase_x, purchase_y, option_x, option_y):
        """세부 선택지 있는 구매 상품"""
        try:
            print(f"구매 버튼 클릭 좌표: ({purchase_x}, {purchase_y})")
            self.driver.tap([(purchase_x, purchase_y)])
            time.sleep(4)

            # 선택지 클릭
            print(f"선택지 클릭 좌표: ({option_x}, {option_y})")
            self.driver.tap([(option_x, option_y)])
            time.sleep(4)

            # 구매 취소 버튼 클릭
            print("구매 취소 버튼 클릭")
            self.driver.tap([(530, 200)])
            time.sleep(4)

            # 추가 버튼 클릭
            print("추가 버튼 클릭")
            self.driver.tap([(545, 1835)])
            time.sleep(4)

            return True
        except Exception as e:
            print(f"구매 프로세스 실패: {str(e)}")
            return False

    def click_purchase_button(self, x, y):
        """구매 버튼 클릭 후 취소"""
        try:
            print(f"구매 버튼 클릭 좌표: ({x}, {y})")
            self.driver.tap([(x, y)])
            time.sleep(4)

            # 구매 취소 버튼 클릭
            print("구매 취소 버튼 클릭")
            self.driver.tap([(530, 200)])
            time.sleep(4)

            return True
        except Exception as e:
            print(f"구매 버튼 클릭 또는 취소 실패: {str(e)}")
            return False

    def test_iap_flow(self):
        """
        인앱 결제 플로우 테스트

        테스트 항목:
        1. 상점 진입
        2. 첫 화면 상품 (3개) 구매 버튼 테스트
        3. 첫 번째 스크롤 후 상품 (2개) 구매 버튼 테스트
        4. 두 번째 스크롤 후 상품 (4개) 구매 버튼 테스트
        5. 세 번째 스크롤 후 상품 (3개) 구매 버튼 테스트

        총 12개의 구매 테스트
        """
        try:
            # 1. 게임 실행 대기
            time.sleep(3)

            # 2. 상점 진입
            assert self.enter_shop(), "상점 진입 실패"
            time.sleep(2)

            # 3. 스크롤별 구매 버튼 테스트
            print("\n구매 버튼 테스트 시작...")

            # 스크롤 전 첫 화면
            # 첫 번째 상품 - 첫 번째 선택지
            assert self.click_purchase_button_with_option(764, 1148, 300, 1545), "첫 번째 선택지 테스트 실패"
            time.sleep(4)

            # 첫 번째 상품 - 두 번째 선택지
            assert self.click_purchase_button_with_option(764, 1148, 800, 1545), "두 번째 선택지 테스트 실패"
            time.sleep(4)

            # 두 번째 상품 (일반 구매)
            assert self.click_purchase_button(777, 1840), "두 번째 상품 구매 테스트 실패"
            time.sleep(4)

            # 첫 번째 스크롤
            assert self.scroll_down(), "첫 번째 스크롤 실패"
            time.sleep(4)
            purchase_buttons = [
                (777, 1183),
                (777, 1876)
            ]
            for x, y in purchase_buttons:
                assert self.click_purchase_button(x, y), "구매 버튼 클릭 실패"
                time.sleep(4)

            # 두 번째 스크롤
            assert self.scroll_down(), "두 번째 스크롤 실패"
            time.sleep(4)
            purchase_buttons = [
                (777, 1148),
                (232, 1983),
                (554, 1983),
                (871, 1983)
            ]
            for x, y in purchase_buttons:
                assert self.click_purchase_button(x, y), "구매 버튼 클릭 실패"
                time.sleep(4)

            # 세 번째 스크롤
            assert self.scroll_down(), "세 번째 스크롤 실패"
            time.sleep(4)
            purchase_buttons = [
                (232, 1079),
                (549, 1079),
                (866, 1079)
            ]
            for x, y in purchase_buttons:
                assert self.click_purchase_button(x, y), "구매 버튼 클릭 실패"
                time.sleep(4)

            print("\n모든 구매 버튼 테스트 완료!")

        except Exception as e:
            self.driver.save_screenshot('iap_error.png')
            raise e