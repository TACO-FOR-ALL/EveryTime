# POSTS-API 목록

- [POSTS-API 목록](#posts-api-목록)
  - [실시간베스트게시글목록](#실시간베스트게시글목록)
  - [게시글내용요청](#게시글내용요청)

## 실시간베스트게시글목록

>***LOGIN_NEEDED***

- **URL**: `/posts/get_realtime_best`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**:
```json
{
    "posts": [
      {
        "url": "string",
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
|posts-url|string|미리보기 이미지 다운로드 url|
|posts-title|string|게시글 제목|
|posts-post_id|string|게시글 id|
|posts-board_name|string|게시판 명칭|

## 게시글내용요청

>***LOGIN_NEEDED***

- **URL**: `/posts/get/?postid=<id>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**:
```json
{
    "posts": [
      {
        "url": "string",
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
|posts-url|string|미리보기 이미지 다운로드 url|
|posts-title|string|게시글 제목|
|posts-post_id|string|게시글 id|
|posts-board_name|string|게시판 명칭|