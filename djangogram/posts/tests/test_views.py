from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

class TestPosts(TestCase):
    # POST 방식에 이용되는 사용자 초기화 및 생성 코드
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="jungo", email="jungo@gmail.com", password="top_secret"
        )

    # GET 방식 TEST 코드
    def test_get_posts_page(self):
        url = reverse('posts:post_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_create.html')

    # POST 방식 TEST 코드.
    # client가 우리를 대신해서 서버에 요청(post방식)을 함.
    # 결과값(response)은 실제 사용자가 받는 결과값임. 그 결과값이 예상되는 값(200)과 맞는지, html로 가는지 확인.
    def test_post_creating_posts(self): # 테스트한다_post방식을_만드는걸로_posts(게시글)을

        # 로그인 코드
        login = self.client.login(username="jungo", password="top_secret")
        self.assertTrue(login)

        # 데이터 처리 코드
        url = reverse('posts:post_create')
        image = SimpleUploadedFile("test.jpg", b"whatevercontents") # 이 코드 쓰면 이미지 파일을 굳이 다운 받아 우리 폴더에 넣지 않아도 이미지 가져옴. (이미지 이름, 이미지 내용(바이너리로 저장됨. 테스트할 땐 큰 의미없는 단어임.))
        response = self.client.post(
            url,
            {"image": image, "caption": 'test test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/base.html")

    def test_post_posts_create_not_login(self):
        url = reverse('posts:post_create')
        image = SimpleUploadedFile("test.jpg", b"whatevercontents")
        response = self.client.post(
            url,
            {"image": image, "caption": 'test test'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/main.html")
