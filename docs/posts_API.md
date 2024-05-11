# POSTS-API 목록

- [POSTS-API 목록](#posts-api-목록)
  - [실시간베스트게시글목록](#실시간베스트게시글목록)
  - [게시글내용요청](#게시글내용요청)

## 실시간베스트게시글목록

>***LOGIN_NEEDED***

- **URL**: `/posts/realtime_best`
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
- **REOUEST PAYLOAD**:
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
        "created_at": "string"
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