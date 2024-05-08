# BOARDS-API 목록- [BOARDS-API 목록](#boards-api-목록)

- [BOARDS-API 목록- BOARDS-API 목록](#boards-api-목록--boards-api-목록)
  - [메인게시판요청](#메인게시판요청)
  - [즐겨찾는게시판요청](#즐겨찾는게시판요청)


## 메인게시판요청

>***LOGIN_NEEDED***

- **URL**: `/boards/main_board`
- **METHOD**: `GET`
- **REQUEST PAYLOAD**:
```json
None
```
- **RESPONSE PAYLOAD**: **기본 형식**

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

- **URL**: `/boards/bookmark_boards`
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