# POSTS-API 목록

- [POSTS-API 목록](#posts-api-목록)
  - [실시간베스트게시글목록](#실시간베스트게시글목록)
  - [게시글내용요청](#게시글내용요청)
  - [게시글업로드](#게시글업로드)
  - [게시글업로드실패고지](#게시글업로드실패고지)

## 실시간베스트게시글목록

>***LOGIN_NEEDED***

- **URL**: `/posts/realtime_best`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**:
```json
{
    "posts": [
      {
        "is_media": bool,
        "title": "string",
        "post_id": "string",
        "board_name": "string"
      }
    ]
}
```

|이름|타입|설명|
| - | - | - |
|posts|array|(리스트 획득 성공 시)실시간 베스트 게시글 list, 각 원소는 1개 게시글을 대표함|
|posts-is_media|string|사진 첨부 여부, true 시 첨부|
|posts-title|string|게시글 제목|
|posts-post_id|string|게시글 id|
|posts-board_name|string|게시판 명칭|

## 게시글내용요청

>***LOGIN_NEEDED***

- **URL**: `/posts/get/?postid=<id>`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|postid|string|내용을 요청하는 게시글의 id|
- **RESPONSE PAYLOAD**:
```json
{
    "post": [
      {
        "media_urls":[
          "string",
          ...
        ],
        "title": "string",
        "board_name": "string",
        "board_id": "string",
        "created_at": "string",
        "nickname": "string"
      }
    ]
}
```
|이름|타입|설명|
| - | - | - |
|posts-media_urls|array|사진/영상 등 게시물 첨부물(첨부물 없을 시 빈 Array)|
|posts-title|string|게시글 제목|
|posts-board_name|string|게시판 명칭|
|posts-board_id|string|게시판 id|
|posts-created_at|string|게시글 등록 시간(가독 format)|
|posts-nickname|string|게시글 작성자 노출명 nickname, 익명 게시글인 경우 빈값, 본인 게시글인 경우 '나'|


## 게시글업로드

>***LOGIN_NEEDED***

- **URL**: `/posts/upload`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
  "board_id": "string",
  "title": "string",
  "anonymous": bool,
  "content": "string",
  "file_num": int
}
```
|이름|타입|설명|
| - | - | - |
|board_id|string|해당 게시글을 업로드하고자 하는 게시글 id|
|title|string|게시글 제목|
|anonymous|string|게시글 익명 여부, True일 시 익명|
|content|string|게시글 내용 (텍스트), 렌더링에 필요한 격식 그대로 전송 요망|
|file_num|int|업로드하고자 하는 사진/영상 개수|

- **RESPONSE PAYLOAD**:
```json
{
  "data": {
    "medias": [
      {
        "upload_url": "string",
        "callback_url": "string",
        "callback_payload": "string"
      }
    ],
    "post_id": "string"
  }
}
```
|이름|타입|설명|
| - | - | - |
|medias|array|각 사진/영상의 업로드에 필요한 정보, 각 원소는 1개 사진/영상에 해당되는 정보를 나타냄, 요청의 file_num이 0일 시, 빈 리스트|
|medias-upload_url|array|요청한 `file_num`에 해당되는 만큼의 업로드에 사용할 url|
|medias-callback_url|string|OSS로 업로드 요청 시, 업로드 성공 후 OSS서버에서 callback 요청을 보낼 url, 사용 시 https://<SERVER_DOMAIN><callback_url> 형식을 사용 (SERVER_DOMAIN은 백엔드 서버 도메인)|
|medias-callback_payload|string|OSS로 업로드 요청 시, 업로드 성공 후 OSS 서버에서 callback 요청을 보낼 때 사용할 payload, 그대로 사용|
|post_id|string|등록된 게시글 id|

**주의1:** 주어진 upload_urls로 **업로드에 실패**한 경우, **[게시글 업로드 실패 고지 요청](#게시글업로드실패고지) 발송 필수**

**주의2:** upload 성공 시까지 해당 게시글은 **열람 불가** 상태, upload에 성공하면 **OSS서버에서 백엔드 서버에 고지**, 해당 시점부터 열람 가능

**주의3:** `medias`리스트 내의 정보들을 유저가 업로드한 사진/영상 순서에 따라 

**주의4:** callback_url 사용 참고 자료: `https://help.aliyun.com/zh/oss/developer-reference/callback?spm=a2c4g.11186623.0.i5#reference-zkm-311-hgb`

## 게시글업로드실패고지

>***LOGIN_NEEDED***

- **URL**: `/posts/upload/fail/?postid=<postid>`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|postid|string|관련 미디어 업로드에 실패한 게시글 id|

- **RESPONSE PAYLOAD**: **기본 형식**