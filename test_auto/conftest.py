import pytest
from datetime import datetime
import pandas as pd
import os


def pytest_sessionstart(session):
    """테스트 세션 시작 시 실행"""
    # 결과를 저장할 빈 DataFrame 생성
    session.results = []


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":  # 테스트 실행 단계에서만 기록
        # 현재 시간
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 테스트 결과 저장
        item.session.results.append({
            'Timestamp': timestamp,
            'Test Name': item.name,
            'Result': 'Pass' if result.passed else 'Fail',
            'Duration': f"{result.duration:.2f}s"
        })


def pytest_sessionfinish(session):
    """테스트 세션 종료 시 실행"""
    if hasattr(session, 'results'):
        # DataFrame 생성
        df = pd.DataFrame(session.results)

        # 파일 경로 설정
        file_path = 'test_results.xlsx'

        # 기존 파일이 있으면 읽어서 합치기
        if os.path.exists(file_path):
            existing_df = pd.read_excel(file_path)
            df = pd.concat([existing_df, df], ignore_index=True)

        # 결과를 엑셀 파일로 저장
        df.to_excel(file_path, index=False)
        print(f"\n테스트 결과가 {file_path}에 저장되었습니다.")