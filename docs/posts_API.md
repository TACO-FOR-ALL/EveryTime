# POSTS-API 목록

- [POSTS-API 목록](#posts-api-목록)
  - [메인게시판요청](#메인게시판요청)
  - [즐겨찾는게시판요청](#즐겨찾는게시판요청)
  - [실시간베스트게시글목록](#실시간베스트게시글목록)
  - [게시글내용요청](#게시글내용요청)

## 메인게시판요청

>***LOGIN_NEEDED***

- **URL**: `/posts/main_board`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**: **기본 형식**

```json
{
    "board_name": "string",
    "board_id": "string"
}
```
|이름|타입|설명|
| - | - | - |
|borad_name|string|메인 게시판 이름|
|board_id|string|메인 게시판 id|

## 즐겨찾는게시판요청

>***LOGIN_NEEDED***

- **URL**: `/posts/bookmark_boards`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**: **기본 형식**

```json
{
    "boards": [
        {
            "board_name": "string",
            "board_id": "string"
        },
        ...
    ]
}
```
|이름|타입|설명|
| - | - | - |
|boards|array|(리스트 획득 성공 시)즐겨찾기 게시판 list, 각 원소는 1개 게시판을 대표함|
|boards-borad_name|string|즐겨찾기 게시판 이름|
|boards-board_id|string|즐겨찾기 게시판 id|

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