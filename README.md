# Mate365 Billing Portal Web App

## 개발환경 설정

Python 3.x 필요

```bash
# Python virtualenv 가상환경 진입
. venv/bin/activate

# 가상 환경에 의존성 받기
pip install -r requirements.txt

# DB 테이블 생성 스크립트 생성
python manage.py makemigrations

# DB 테이블 생성
python manage.py migrate

# 로컬에서 테스트 서버 실행
python manage.py runserver
# 또는 python3 manage.py runserver

# 가상환경 나오기
deactivate
```

## 환경변수

- `DJANGO_SETTINGS_MODULE`: 백엔드 실행시 사용할 설정 모듈
    - 환경변수 설정 없는 경우, 개발용 설정 모듈을 기본값으로 사용
    - `Mate365BillingPortal.settings.dev`: 개발용 설정(SQLite)
    - `Mate365BillingPortal.settings.prod`: 프로덕션용 설정(MS-SQL)
- DB 연결 정보(프로덕션 설정 사용시만 해당)
    - `DB_HOST`: 데이터베이스 접속 주소 또는 호스트명
        - 예: `localhost\SQLEXPRESS`, `1.2.3.4`
    - `DB_NAME`: 접속할 데이터베이스 이름
    - `DB_USER`: 인증에 사용할 로그인 사용자명
    - `DB_PASSWORD`: 인증에 사용할 로그인 암호
    - `DB_DRIVER`: 사용할 데이터베이스 드라이버
        - `ODBC Driver 13 for SQL Server` - 기본값
        - `SQL Server Native Client 11.0`
        - `FreeTDS`
        