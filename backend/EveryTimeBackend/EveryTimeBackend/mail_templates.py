def get_html_content(content):
    return f"""
<html>
<body>
<p>안녕하세요,<br>
{content}<br><br>
본 이메일은 북경 커뮤니티 이용에 필요한 본인확인 절차를 위해 발송되었습니다.<br>
모바일 애플리케이션에서 상기 코드를 입력한 뒤 회원가입을 완료하여 주시기 바랍니다.<br>
본 메일은 발신 전용 메일로 회신이 불가능합니다. 문의사항이 있으시면 고객센터/아래 연락처를 이용하여 주시기 바랍니다.
</p>
</body>
</html>
"""
