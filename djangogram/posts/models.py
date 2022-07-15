
from django.db import models
from djangogram.users import models as user_model

# Create your models here.
class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta: # 이 클래스를 사용하면 해당 클래스는 테이블을 만들지 않음.
        abstract = True

# 장고는 흔히 게시물 생성 시간과 수정 시간을 가짐. 각각의 클래스에 이걸 매번 추가하지 않고 시간관련 부분을 클래스로 따로 만들어서 관리하자.
# 시간관련 클래스 만들고 상속하면 됨.

class Post(TimeStamedModel):
    author = models.ForeignKey(
                user_model.User,
                null=True,
                on_delete=models.CASCADE,
                related_name= 'post_author'
            )
    image = models.ImageField(blank=False)
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(
                    user_model.User,
                    blank=True, # 이미지 좋아요 부분 blank를 true로 변경
                    related_name='post_image_likes'
            )

    # 모델을 구분할 수 있게 str 메서드 추가.
    def __str__(self):
        return f"{self.author}: {self.caption}"


class Comment(TimeStamedModel):
    author = models.ForeignKey(
            user_model.User,
            null=True,
            on_delete=models.CASCADE,
            related_name= 'comment_author'
        )
    posts = models.ForeignKey(
            Post,
            null=True,
            on_delete=models.CASCADE,
            related_name= 'comment_post'
        )
    contents = models.TextField(blank=True)

    # 모델을 구분할 수 있게 str 메서드 추가.
    def __str__(self):
        return f"{self.author}: {self.contents}"
