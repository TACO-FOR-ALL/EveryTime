# BOARDS-API 목록- [BOARDS-API 목록](#boards-api-목록)

- [BOARDS-API 목록- BOARDS-API 목록](#boards-api-목록--boards-api-목록)
  - [메인게시판요청](#메인게시판요청)
  - [즐겨찾는게시판요청](#즐겨찾는게시판요청)
  - [메인게시판조작](#메인게시판조작)
  - [즐겨찾기게시판조작](#즐겨찾기게시판조작)
  - [특정게시판내게시글정보요청](#특정게시판내게시글정보요청)


## 메인게시판요청

>***LOGIN_NEEDED***

- **URL**: `/boards/get/main_board`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**:

```json
{
    "main_board":{
        "board_name": "string",
        "board_id": "string"
    }
}
```
|이름|타입|설명|
| - | - | - |
|borad_name|string|메인 게시판 이름(설정된 메인 게시판이 없을 경우 빈 값)|
|board_id|string|메인 게시판 id|

## 즐겨찾는게시판요청

>***LOGIN_NEEDED***

- **URL**: `/boards/get/bookmark_boards`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**:

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

## 메인게시판조작

>***LOGIN_NEEDED***

- **URL**: `/boards/set/main_board`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "main_board":{
        "board_id": "string",
        "is_delete": bool
    }
}
```
|이름|타입|설명|
| - | - | - |
|main_board-board_id|string|설정할 메인 게시판 id(삭제 조작일 시 빈 값)|
|main_board-is_delete|bool|삭제 조작일 시 true, 추가(변경) 조작일 시 false|
- **RESPONSE PAYLOAD**: **기본 형식**

## 즐겨찾기게시판조작

>***LOGIN_NEEDED***

- **URL**: `/boards/set/main_board`
- **METHOD**: `POST`
- **REQUEST PAYLOAD**:
```json
{
    "favorite_board":{
        "board_id": "string",
        "is_delete": bool
    }
}
```
|이름|타입|설명|
| - | - | - |
|favorite_board-board_id|string|설정할 즐겨찾기 게시판 id(삭제 조작일 시 빈 값)|
|favorite_board-is_delete|bool|삭제 조작일 시 true, 추가 조작일 시 false|
- **RESPONSE PAYLOAD**: **기본 형식**

## 특정게시판내게시글정보요청

>***LOGIN_NEEDED***

- **URL**: `/boards/get/posts/?boardid=<id>&timestamp=<timestamp>&num=<num>&keyword=<keyword>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|boardid|string|(필수)게시글을 요청하는 게시판의 id|
|timestamp|string|Pagination을 위한, 마지막으로 표시한 게시글에 해당되는 timestamp, 첫 요청 시 미포함|
|num|int|(필수)요청하는 게시글의 수량|
|keyword|string|찾고자 하는 게시글 관련 keyword(작성자 닉네임/게시글 제목/게시글 내용), 비검색 요청 시 미포함|
- **RESPONSE PAYLOAD**:
```json
{
    "posts": [
      {
        "is_media": bool,
        "title": "string",
        "post_id": "string",
        "board_name": "string",
        "board_id": "string",
        "timestamp": "string",
        "created_at": "string"
      }
    ]
}
```
|이름|타입|설명|
| - | - | - |
|posts|array|(리스트 획득 성공 시)실시간 베스트 게시글 list, 각 원소는 1개 게시글을 대표함|
|posts-is_media|string|사진/영상 첨부 여부, True 시 첨부|
|posts-title|string|게시글 제목|
|posts-post_id|string|게시글 id|
|posts-board_name|string|게시판 명칭|
|posts-board_id|string|게시판 id|
|posts-timestamp|string|게시글의 timestamp, Pagination에 사용|
|posts-created_at|string|게시글 등록 시간, 가독 format|