# 카테고리

>모든 PAYLOAD는 JSON form을 사용

1. [계정](#계정)
    

## 계정

- [로그인](#로그인)
- [회원가입](#회원가입)
- [가입가능학교리스트](#가입가능학교리스트)
- [인증용이메일리스트요청](#인증용이메일리스트요청)
- [인증메일발송요청](#인증메일발송요청)
- [인증코드확인요청](#인증코드확인요청)
- [비밀번호리셋인증메일발송요청](#비밀번호리셋인증메일발송요청)

### 로그인

- **URL**: `/users/login`
- **METHOD**: `POST`
- **REOUEST PAYLOAD**:
```json
{
    "id":"string",
    "password":"string"
}
```
|이름|타입|설명|
| - | - | - |
|id|string|사용자ID|
|password|string|사용자PW|

- **RESPONSE PAYLOAD**:
```json
{
    "status":"int",
    "session":"string(uuid)",
    "error_msg":"string"
}
```

|이름|타입|설명|
| - | - | - |
|status|int|0: 로그인 성공 (session제공); 1: 로그인 실패 (error_msg 제공)|
|session|string|(로그인 성공 시)세션ID|
|error_msg|string|(로그인 실패 시)로그인 실패 원인|

### 회원가입

- **URL**: `/users/signup`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "id":"string",
    "password":"string",
    "email":"string",
    "organization": "string"
    // TODO: 기타 정보 제공?
}
```
|이름|타입|설명|
| - | - | - |
|id|string|사용자ID|
|password|string|사용자PW|
|email|string|사용자 이메일|
|organization_id|string|사용자 소속 학교/단체 id|

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "error_msg": "string"
}
```
|이름|타입|설명|
| - | - | - |
|status|int|0 - 회원가입 성공; 1 - 회원가입 실패 (error_msg제공)|
|error_msg|string|(회원가입 실패 시)회원가입 실패 원인|

- **추가 정보**
    - front에서 동일 **비밀번호 2회 입력** 후 동일한지 확인 필요

### 가입가능학교리스트

- **URL**: `/users/organization/list`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "organizations": [
        {
            "name": "string",
            "region": "string",
            "id": "string"
            // TODO: 추가 정보?
        },
        ...
    ],
    "error_msg": "string"
}
```
|이름|타입|설명|
| - | - | - |
|status|int|0 - 성공; 1 - 실패 (error_msg 제공)|
|organizations|array|가입 가능 학교/단체 list, 각 원소는 1개 학교/단체를 대표함|
|organizations-name|string|학교/단체 이름|
|organizations-region|string|학교/단체 소속 지역|
|organizations-id|string|학교/단체 id (인증용 이메일 request에 사용)|
|error_msg|string|요청 처리 실패 원인|


### 인증용이메일리스트요청

- **URL**: `/users/organization/emails`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "org_id":"string"
}
```
|이름|타입|설명|
| - | - | - |
|org_id|string|인증용 이메일 리스트를 요청할 학교/단체의 id|

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "emails":[
        "string",
        "string",
        ...
    ],
    "error_msg": "string"
}
```
|이름|타입|설명|
| - | - | - |
|status|int|0 - 성공; 1 - 실패 (error_msg 제공)|
|emails|array|인증용 이메일 list, 각 원소는 1개 이메일을 뜻함|
|error_msg|string|요청 처리 실패 원인|

### 인증메일발송요청

- **URL**: `/users/organization/send_auth_email`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "organization_id": "string",
    "email":"string"
}
```
|이름|타입|설명|
| - | - | - |
|organization_id|string|사용자가 소속된 단체 id|
|email|string|인증메일을 발송할 이메일 주소(suffix 포함), 사용자 제공|

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "error_msg": "string"
}
```
|이름|타입|설명|
| - | - | - |
|status|int|0 - 발송 성공; 1 - 발송 실패 (error_msg제공)|
|error_msg|string|인증 메일 발송 실패 원인|

### 인증코드확인요청

- **URL**: `/users/organization/check_auth_code`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "email": "string",
    "code":"string"
}
```
|이름|타입|설명|
| - | - | - |
|email|string|인증 코드를 수신한 이메일 주소|
|code|string|인증 코드|

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "error_msg": "string"
}
```
|이름|타입|설명|
| - | - | - |
|status|int|0 - 인증 성공; 1 - 인증 실패 (error_msg제공)|
|error_msg|string|코드 인증 실패 원인|

### 비밀번호리셋인증메일발송요청

- **URL**: `/users/reset-password/send_auth_mail`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "email": "string"
}
```
|이름|타입|설명|
| - | - | - |
|email|string|가입 시 사용한 이메일|

- **RESPONSE PAYLOAD**:
```json
{
    "status": "int",
    "error_msg": "string"
}
```
|이름|타입|설명|
|status|int|0 - 인증 메일 발송 성공; 1 - 인증 메일 발송 실패 (error_msg제공)|
|error_msg|string|인증 메일 발송 실패 원인|