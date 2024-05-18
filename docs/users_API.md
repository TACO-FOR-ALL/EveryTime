# USERS-API 목록

- [USERS-API 목록](#users-api-목록)
  - [로그인](#로그인)
  - [JWT토큰갱신](#jwt토큰갱신)
  - [회원가입](#회원가입)
  - [가입가능학교리스트](#가입가능학교리스트)
  - [가입인증용이메일리스트요청](#가입인증용이메일리스트요청)
  - [가입인증메일발송요청](#가입인증메일발송요청)
  - [가입인증코드확인요청](#가입인증코드확인요청)
  - [비밀번호리셋인증메일발송요청](#비밀번호리셋인증메일발송요청)
  - [비밀번호리셋인증메일확인요청](#비밀번호리셋인증메일확인요청)
  - [비밀번호리셋요청](#비밀번호리셋요청)
  - [비익명게시글노출명요청](#비익명게시글노출명요청)
  - [비익명게시글노출명설정](#비익명게시글노출명설정)

## 로그인

>JWT refresh/access token 획득 API

- **URL**: `/users/login`
- **METHOD**: `POST`
- **REOUEST PAYLOAD**:
```json
{
    "username":"string",
    "password":"string"
}
```
|이름|타입|설명|
| - | - | - |
|username|string|사용자ID|
|password|string|사용자PW|

- **RESPONSE PAYLOAD**:
```json
{
    "tokens": {
        "refresh": "string",
        "access": "string"
    }
}
```

|이름|타입|설명|
| - | - | - |
|tokens|dict|(로그인 성공 시) jwt 인증용 token|
|tokens:refresh|string|jwt refresh token|
|tokens:access|string|jwt access token|

## JWT토큰갱신

>JWT access token 갱신(REFRESH) API

- **URL**: `/users/refresh-access-token`
- **METHOD**: `POST`
- **REOUEST PAYLOAD**:
```json
{
    "refresh":"string"
}
```
|이름|타입|설명|
| - | - | - |
|refresh|string|jwt refresh token|

- **RESPONSE PAYLOAD**:
```json
{
    "access": "string"
}
```

|이름|타입|설명|
| - | - | - |
|access|string|(갱신 성공 시) 새로운 jwt access token|

## 회원가입

- **URL**: `/users/signup`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "username":"string",
    "password":"string",
    "nickname": "string",
    "email":"string",
    "organization_id": "string"
}
```
|이름|타입|설명|
| - | - | - |
|username|string|사용자ID, 로그인에 사용|
|password|string|사용자PW|
|nickname|string|사용자 닉네임, 비익명 게시글 작성 시에 사용할 nickname|
|email|string|사용자 이메일|
|organization_id|string|사용자 소속 학교/단체 id|

- **RESPONSE PAYLOAD**: **기본 형식**

- **추가 정보**
    - front에서 동일 **비밀번호 2회 입력** 후 동일한지 확인 필요


## 가입가능학교리스트

- **URL**: `/users/organization/list`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```

- **RESPONSE PAYLOAD**:
```json
{
    "organizations": [
        {
            "name": "string",
            "region": "string",
            "id": "string"
            // TODO: 추가 정보?
        },
        ...
    ]
}
```
|이름|타입|설명|
| - | - | - |
|organizations|array|(리스트 획득 성공 시)가입 가능 학교/단체 list, 각 원소는 1개 학교/단체를 대표함|
|organizations-name|string|학교/단체 이름|
|organizations-region|string|학교/단체 소속 지역|
|organizations-id|string|학교/단체 id (인증용 이메일 request에 사용)|


## 가입인증용이메일리스트요청

- **URL**: `/users/organization/emails/?orgid=<org_id>`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|org_id|string|인증용 이메일 리스트를 요청할 학교/단체의 id|

- **RESPONSE PAYLOAD**:
```json
{
    "emails":[
        "string",
        "string",
        ...
    ]
}
```
|이름|타입|설명|
| - | - | - |
|emails|array|(리스트 획득 성공 시)인증용 이메일 list, 각 원소는 1개 이메일을 뜻함|

## 가입인증메일발송요청

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

- **RESPONSE PAYLOAD**: **기본 형식**

## 가입인증코드확인요청

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

- **RESPONSE PAYLOAD**: **기본 형식**

## 비밀번호리셋인증메일발송요청

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

- **RESPONSE PAYLOAD**: **기본 형식**

## 비밀번호리셋인증메일확인요청

- **URL**: `/users/reset-password/check_auth_code`
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

- **RESPONSE PAYLOAD**: **기본 형식**

## 비밀번호리셋요청

- **URL**: `/users/reset-password/set_password`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "email": "string",
    "password": "string"
}
```
|이름|타입|설명|
| - | - | - |
|email|string|인증 코드를 수신한 이메일 주소|
|password|string|새 비밀번호|

- **RESPONSE PAYLOAD**: **기본 형식**

## 비익명게시글노출명요청

>***LOGIN_NEEDED***

- **URL**: `/users/nickname`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```

**주의**: 본인의 노출명만 요청 가능

- **RESPONSE PAYLOAD**:
```json
{
    "nickname": "string"
}
```
|이름|타입|설명|
| - | - | - |
|nickname|string|본인의 비익명 게시글 노출명|

## 비익명게시글노출명설정

>***LOGIN_NEEDED***

- **URL**: `/users/nickname`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "nickname": "string"
}
```
|이름|타입|설명|
| - | - | - |
|nickname|string|새로 설정할 노출명|

**주의**: 본인의 노출명만 설정 가능

- **RESPONSE PAYLOAD**: **기본 형식**

**주의**: 비익명 게시글 노출명은 **1달에 1번만 변경이 가능**하며, **설정 후 삭제 불가**, 적어도 2글자 이상의 이름을 설정할 것