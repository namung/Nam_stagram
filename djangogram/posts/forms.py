from django import forms
from .models import Post, Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption", "image"] # 내용작성은 models.py 참고!

        labels = {
            "caption" : "내용",
            "image" : "사진"
        }

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]

class CommentForm(forms.ModelForm):
    # label이 원래는 contents 인데 그 글자를 보여주고 싶지 않아서 contents를 재정의함.
    contents = forms.CharField(widget=forms.Textarea, label="")

    class Meta:
        model = Comment
        fields = ["contents"]
