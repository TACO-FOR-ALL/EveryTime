# BOARDS-API 목록- [BOARDS-API 목록](#boards-api-목록)

- [BOARDS-API 목록- BOARDS-API 목록](#boards-api-목록--boards-api-목록)
  - [메인게시판요청](#메인게시판요청)
  - [즐겨찾는게시판요청](#즐겨찾는게시판요청)
  - [메인게시판조작](#메인게시판조작)
  - [즐겨찾기게시판조작](#즐겨찾기게시판조작)


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
        "board_name": "string",
        "board_id": "string",
        "is_delete": bool
    }
}
```
|이름|타입|설명|
| - | - | - |
|main_board-borad_name|string|메인 게시판 이름(설정된 메인 게시판이 없을 경우 빈 값)|
|main_board-board_id|string|메인 게시판 id|
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
        "board_name": "string",
        "board_id": "string",
        "is_delete": bool
    }
}
```
|이름|타입|설명|
| - | - | - |
|favorite_board-borad_name|string| 게시판 이름(설정된 메인 게시판이 없을 경우 빈 값)|
|favorite_board-board_id|string|메인 게시판 id|
|favorite_board-is_delete|bool|삭제 조작일 시 true, 추가 조작일 시 false|
- **RESPONSE PAYLOAD**: **기본 형식**