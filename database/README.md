# EveryTime앱 Databse

## Infrastructure

- 데이터베이스: `MySQL>=8.0.11`
    - `Django==5.0.3` 요구 사항
    - 현재 `MySQL 8.0.36` 사용 중

## 구축 및 연결 방법 

>Windows 로컬 서버 (개발용) 기준

1. 알맞는 버전의 `MySQL Server` 컴포넌트 설치
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
    - `CREATE DATABASE <db_name> DEFAULT CHARSET utf8 COLLATE utf8_general_ci;`
        - Django는 utf8 charset을 요구
        - utf8_general_ci는 case-insensitive comparison을 의미하지만, case-sensitive collation 선택 시, 잠재적 오류 가능성 有
4. Django Backend `settings.py`의 `DATABASES` 설정에 `DB` 관련 정보 입력
5. 현재 Django Backend에 등록된 App들의 Table을 목표 DB에 생성
    - `python manage.py migrate`