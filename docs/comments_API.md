# COMMENTS-API 목록

## 특정게시글내댓글요청
- [COMMENTS-API 목록](#comments-api-목록)
  - [특정게시글내댓글요청](#특정게시글내댓글요청)
  - [특정댓글의답글요청](#특정댓글의답글요청)
  - [게시글댓글작성](#게시글댓글작성)
  - [댓글답글작성](#댓글답글작성)
  - [댓글좋아요/좋아요해제](#댓글좋아요좋아요해제)
  - [댓글삭제](#댓글삭제)

>***LOGIN_NEEDED***

- **URL**: `/comments/get/comments/?postid=<id>&timestamp=<timestamp>&num=<num>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|postid|string|(필수)댓글을 요청하는 게시글의 id|
|timestamp|string|Pagination을 위한, 마지막으로 표시한 댓글에 해당되는 timestamp, 첫 요청 시 미포함|
|num|int|(필수),요청하는 댓글의 수량|

- **RESPONSE PAYLOAD**:
```json
{
    "comments": [
      {
        "comment_id": "string",
        "author_num": "int",
        "content": "string",
        "timestamp": "string",
        "created_at": "string",
        "reply_num": "int",
        "is_deleted": bool
      }
    ]
}
```
|이름|타입|설명|
| - | - | - |
|comments|array|(리스트 획득 성공 시)댓글 list, 각 원소는 1개 댓글을 나타냄|
|comments-comment_id|string|해당 댓글의 id|
|comments-author_num|string|댓글을 작성한 유저의 해당 게시글 하 임시 id, 작성자는 0|
|comments-content|string|댓글 내용, 삭제되었을 시 빈값|
|comments-timestamp|string|댓글의 timestamp, Pagination에 사용|
|comments-created_at|string|댓글 등록 시간, 가독 format|
|comments-likes|int|댓글이 받은 좋아요 갯수|
|comments-reply_num|string|해당 댓글에 달린 답글 수량, 답글 없을 시 0|
|comments-is_deleted|bool|삭제 여부, 삭제 시 True|

**주의**: 게시글에 대한 직접적인 댓글만 리턴, 각 댓글에 대한 답글은 [해당 API](#특정댓글의답글요청) 활용 요망

## 특정댓글의답글요청

>***LOGIN_NEEDED***

- **URL**: `/comments/get/reply/?commentid=<id>&timestamp=<timestamp>&num=<num>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|commentid|string|(필수)답글을 요청하는 댓글의 id|
|timestamp|string|Pagination을 위한, 마지막으로 표시한 답글에 해당되는 timestamp, 첫 요청 시 미포함|
|num|int|(필수),요청하는 답글의 수량|

- **RESPONSE PAYLOAD**:
```json
{
    "comments": [
      {
        "comment_id": "string",
        "author_num": "int",
        "content": "string",
        "timestamp": "string",
        "created_at": "string",
        "reply_num": "int",
        "is_deleted": bool
      }
    ]
}
```
|이름|타입|설명|
| - | - | - |
|comments|array|(리스트 획득 성공 시)답글 list, 각 원소는 1개 답글을 나타냄|
|comments-comment_id|string|해당 답글의 id|
|comments-author_num|string|답글을 작성한 유저의 해당 게시글 하 임시 id, 작성자는 0|
|comments-content|string|답글 내용, 삭제되었을 시 빈값|
|comments-timestamp|string|답글의 timestamp, Pagination에 사용|
|comments-created_at|string|답글 등록 시간, 가독 format|
|comments-likes|int|답글이 받은 좋아요 갯수|
|comments-reply_num|string|해당 답글에 달린 답글 수량, 답글 없을 시 0|
|comments-is_deleted|bool|삭제 여부, 삭제 시 True|

## 게시글댓글작성

>***LOGIN_NEEDED***

- **URL**: `/comments/upload/comment`
- **METHOD**: `POST`
- **REOUEST PAYLOAD**:
```json
{
  "post_id": "string",
  "content": "string"
}
```
|이름|타입|설명|
| - | - | - |
|post_id|string|댓글을 작성하고자 하는 게시글 id|
|content|string|댓글 내용 (렌더링에 필요한 양식 그대로)|

- **RESPONSE PAYLOAD**: **기본 형식**

## 댓글답글작성

>***LOGIN_NEEDED***

- **URL**: `/comments/upload/reply`
- **METHOD**: `POST`
- **REOUEST PAYLOAD**:
```json
{
  "comment_id": "string",
  "content": "string"
}
```
|이름|타입|설명|
| - | - | - |
|comment_id|string|답글을 작성하고자 하는 댓글 id|
|content|string|답글 내용 (렌더링에 필요한 양식 그대로)|

- **RESPONSE PAYLOAD**: **기본 형식**

## 댓글좋아요/좋아요해제

>***LOGIN_NEEDED***

- **URL**: `/comments/like/?commentid=<comment_id>&like=<like>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|comment_id|string|좋아요 설정/해제를 원하는 댓글 id|
|like|int|좋아요 설정 시 1, 좋아요 해제 시 0|

**주의:** 본인 댓글에만 요청 가능

- **RESPONSE PAYLOAD**: **기본 형식**

## 댓글삭제

>***LOGIN_NEEDED***

- **URL**: `/comments/delete/?commentid=<comment_id>`
- **METHOD**: `GET`
- **REOUEST PAYLOAD**:
```json
None
```
|이름|타입|설명|
| - | - | - |
|comment_id|string|삭제하고자 하는 댓글 id|

**주의:** 본인 댓글 또는 해당 게시판 관리자만 요청 가능

- **RESPONSE PAYLOAD**: **기본 형식**