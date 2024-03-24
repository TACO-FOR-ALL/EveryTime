# 카테고리

>모든 PAYLOAD는 JSON form을 사용

1. [계정](#계정)
    - [로그인](#로그인)
    - [회원가입](#회원가입)

## 계정

### 로그인

- **URL**: `/api/user/login`
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

- **URL**: `/api/user/signup`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "id":"string",
    "password":"string",
    "organization": "string"
    // TODO: 기타 정보 제공?
}
```
|이름|타입|설명|
| - | - | - |
|id|string|사용자ID|
|password|string|사용자PW|
|organization|string|사용자 소속 (학교)|

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