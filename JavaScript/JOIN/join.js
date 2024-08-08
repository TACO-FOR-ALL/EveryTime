//제출 이벤트를 받는다.(이벤트 핸들링)
const form = document.getElementById("form");
form.addEventListener("submit", function(e){
    e.preventDefault() //기존 새로고침 기능 차단
    let userId = e.target.id.value;
    let userPw1 = e.target.pw1.value;
    let userPw2 = e.target.pw2.value;
    let userName = e.target.name.value;
    let userPhone = e.target.phone.value;
    let userPosition = e.target.position.value;
    let userGender = e.target.gender.value;
    let userEmail = e.target.email.value;
    let userIntro = e.target.intro.value;
    //제출된 입력 값들을 참조한다.
    //console.log(userId, userPw1,userPw2,userName,userPhone,userPosition,userGender,userEmail,userIntro)
    
    //입력값에 문제가 있는 경우 이를 감지한다   
    if(userId.length < 6){
        alert("아이디가 너무 짧습니다. 6자 이상 입력해주세요.");
        return;
    }
    if(userPw1 !== userPw2){
        alert("비밀번호가 일치하지 않습니다!");
        return;
    }
    
    //모든 조건 충족시 가입 환영 인사 메세지를 출력한다.
    document.body.innerHTML = "";
    document.write(`<p>${userName}님 환영합니다!</p>`)
    document.write(`<p>회원가입시 이력하신 내역은 다음과 같습니다.</p>`)
    document.write(`<p>아이디: ${userId}</p>`)
    document.write(`<p>이름: ${userName}</p>`)
    document.write(`<p>전화번호: ${userPhone}</p>`)
    document.write(`<p>원하는 직무: ${userPosition}</p>`)
})





