# EveryTime앱 Databse

## Infrastructure

- 데이터베이스: `MySQL>=8.0.11`
    - `Django==5.0.3` 요구 사항
    - 현재 `MySQL 8.0.36` 사용 중

## 구축 및 연결 방법 

### Windows 로컬 서버 (개발용)

1. 알맞은 버전의 `MySQL Server` 컴포넌트 설치
    - `MySQL Workbench` 설치 권장
2. Timezone Table 생성 및 Timezone data 입력
    1. 설정에 필요한 SQL 파일 설치 및 압축 해제
        - `https://dev.mysql.com/downloads/timezones.html`
        - 또는, `build` 폴더 내의 `timezone_posix.sql` 사용
    2. Table 생성 및 data 입력 진행
        - `mysql -u root -p mysql < <path_to_unzipped_file>`
    3. 관련 Query를 통해 완료 여부 확인
        - `SELECT COUNT(*) FROM mysql.time_zone_name;`
        - **결과가 '0'이상이어야 함**
3. Django Backend가 사용할 DB 생성
    - `CREATE DATABASE <db_name> DEFAULT CHARSET utf8mb4`
        - Django는 utf8 charset을 요구
4. Django Backend `settings.py`의 `DATABASES` 설정에 `DB` 관련 정보 입력
    - 현재 `DATABASES` 설정은 동 목록의 `database_config.py`로 분리하여 관리, 해당 파일은 깃헙에 업로드하지 않음
5. 현재 Django Backend에 등록된 App들의 Table을 목표 DB에 생성
    - `python manage.py migrate`

### Docker Container 서버 (개발용)
1. 알맞은 버젼의 `MySQL` Image를 Docker Hub에서 Pull
    - 현재 `mysql:8.0.36-debian` 사용 중
2. Container 가동 스크립트 `run_db_in_docker.sh`에 로컬 환경에 맞는 변동사항을 적용하고 실행
3. Django Backend가 사용할 DB 생성
    - 이 부분부터는 [로컬 서버](#windows-로컬-서버-개발용)와 동일