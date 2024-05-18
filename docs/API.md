# 카테고리

1. [계정](users_API.md)
2. [게시판](boards_API.md)
3. [게시글](posts_API.md)
4. [댓글](comments_API.md)
5. [미디어](medias_API.md)

## 동일 양식

1. 모든 REQ/RESP PAYLOAD는 **JSON form**을 사용
2. 모든 리턴에는 기본으로: `status` (status_code)와 (실패 시)`error_msg`가 제공될 예정:
```json
{
    "status": int,
    "error_msg": "string", // if fail
    "...": ... // if any
}
```
이에, 기본적인 `status`나 `error_msg`를 제외한 내용만 각 API의 RESP PAYLOAD에 명시
3. `status`에 포함되는 `status_code`는 다음과 같음.
    - 0: 성공
    - 1: 실패 (`error_msg` 제공)
    - 2: jwt 토큰 미제공 (`error_msg` 제공)
    - 3: jwt access token 만료 또는 식별 불가 token (`error_msg` 제공)
4. 로그인 필요 서비스 (request.head.authorization에 jwt토큰 첨부 필요)는 ***LOGIN_NEEDED*** 표시