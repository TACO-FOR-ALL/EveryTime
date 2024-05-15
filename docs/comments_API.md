# COMMENTS-API 목록

## 특정게시글내댓글요청
- [COMMENTS-API 목록](#comments-api-목록)
  - [특정게시글내댓글요청](#특정게시글내댓글요청)
  - [특정댓글의답글요청](#특정댓글의답글요청)

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
|comments-content|string|댓글 내용|
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
|comments-content|string|답글 내용|
|comments-timestamp|string|답글의 timestamp, Pagination에 사용|
|comments-created_at|string|답글 등록 시간, 가독 format|
|comments-likes|int|답글이 받은 좋아요 갯수|
|comments-reply_num|string|해당 답글에 달린 답글 수량, 답글 없을 시 0|
|comments-is_deleted|bool|삭제 여부, 삭제 시 True|