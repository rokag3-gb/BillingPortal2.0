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
## 테스트 실행
```bash
# 전체 테스트 실행
python manage.py test

# Mate365BillingPortal.tests.EnvtoolsTests 테스트만 실행
python manage.py test Mate365BillingPortal.tests.EnvtoolsTests

# Mate365BillingPortal 디렉터리 아래 테스트만 실행
python manage.py test Mate365BillingPortal/
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
    - `DB_PORT`: DB 접속 포트
    - `DB_DRIVER`: 사용할 데이터베이스 드라이버
        - `ODBC Driver 17 for SQL Server` - App Service 리눅스 환경에서 사용
        - `ODBC Driver 13 for SQL Server` - 기본값
        - `SQL Server Native Client 11.0`
        - `FreeTDS`
- SMTP 이메일 서버 인증 정보
    - `EMAIL_HOST`: SMTP 호스트 주소
    - `EMAIL_PORT`: SMTP 서버 포트(기본값: `587`)
    - `EMAIL_HOST_USER`: SMTP 인증 사용자명
    - `EMAIL_HOST_PASSWORD`: SMTP 인증 암호
    - `EMAIL_FROM`: 이메일 발신 주소
    - `EMAIL_USE_TLS`: 연결에 TLS(포트 `587`) 사용 여부 (기본값: `True`)
    - `EMAIL_USE_SSL`: 연결에 TLS(포트 `465`) 사용 여부 (기본값: `False`)
        - `EMAIL_USE_TLS`, `EMAIL_USE_SSL` 둘 중 하나만 `True` 여야 합니다.
    - `EMAIL_TIMEOUT`: 시간 걸리는 작업 타임아웃 시간(초 단위) (기본값 `None`)
    - `EMAIL_SSL_KEYFILE`: SSL 연결시 사용할 PEM 포맷 자격증명 파일(기본값: `None`)
    - `EMAIL_SSL_CERTFILE`: SSL 연결시 사용할 PEM 포맷 키 파일(기본값: `None`)
- 기타
    - `SECRET_KEY`: 암호 해싱 등에 사용하는 임의 문자열(프로덕션 설정 사용시만 필수)