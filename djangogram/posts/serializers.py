from rest_framework import serializers

from djangogram.users.models import User as user_model
from . import models

# 각각의 model에서 필요한 field에 해당하는 자료를 serializer로 만들어서 가져옴.
class FeedAuthorSerializer(serializers.ModelSerializer): # user 모델을 가지고 있는 시리얼라이저.
    class Meta:
        model = user_model # user 모델을 사용한다고 명시.
        fields = (
            "id",
            "username",
            "profile_photo"
        )

class CommentSerializer(serializers.ModelSerializer):
    author = FeedAuthorSerializer() # author 가 사용하는 user model을 가지고 있는 시리얼라이저 추가.

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "contents",
            "author", # author 추가.
        )

class PostSerializer(serializers.ModelSerializer):
    # comment와 author는 각각 다른 모델 사용해서 각기 다른 serializer를 사용함.
    # 이렇게 하면 serializer가 알아서 db에 접근해서 데이터를 join 해줌.
    comment_post = CommentSerializer(many=True)
    author = FeedAuthorSerializer()

    class Meta:
        # 타겟 모델
        model = models.Post
        # 추출할 field
        fields = (
            "id", # 장고가 default로 생성한 것.
            "image",
            "caption",
            "comment_post", # Comment와 연결됨. Comment에서 post를 외래키로 가지고 있음.
            "author",
            "image_likes",
        )
