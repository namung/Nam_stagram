function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

const handleLikeClick = (buttonId) => {
  console.log(buttonId);

  // 버튼 태그를 가져오는 코드
  const likeButton = document.getElementById(buttonId);

  // likebutton 에서 i 태그 직접 가져옴.
  // querySelector("태그") | (".class") | ("#id")
  const likeIcon = likeButton.querySelector("i");

  // api 전송 전, csrf 토큰 가져옴.
  const csrftoken = getCookie('csrftoken');

  // postId 추출. split 후 pop 하면 마지막 꺼만 가져와짐.
  // like-button-{{ post.id }}
  const postId = buttonId.split("-").pop();

  // url :  /posts/5/post_like/
  // postId는 buttonId에서 가져옴.
  const url = "/posts/" + postId + "/post_like"

  // 서버로 좋아요 api 호출
  // 해당 url로 api 호출. 우리의 요청은 post 요청방식이라 fetch에 option이 필요함.
  fetch(url, {
    method: "POST",
    mode: "same-origin", // 주소가 127.0.0.1:8000 <- 이런식으로 동일하다라는 뜻.
    headers: { // 키 값으로 장고 공식 문서에 따라 X-CSRFToken 이라고 명시.
      'X-CSRFToken': csrftoken
    }
  })
  .then(response => response.json()) // 요청 이후에 받은 결과값을 json으로 변경.
  .then(data => {
    // 결과를 받고 html(좋아요 하트 ) 모습을 변경
    if (data.result === "like") {
      // 좋아요 세팅.
      likeIcon.classList.replace("fa-heart-o", "fa-heart");
    } else {
      // 좋아요 해제.
      likeIcon.classList.replace("fa-heart", "fa-heart-o");
    }
  }); // 이 json 형태로 바꾼 data를 console.log를 통해 찍어줌.
}
