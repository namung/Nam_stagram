from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

# 장고 폼.
class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'username', 'password']

        # label 변경
        # labels = {
        #     'email': "이메일 주소",
        #     'name': "성명",
        #     'username': "사용자 이름",
        #     'password': "비밀번호",
        # }

        # 비밀번호 숫자가 안보이게 설정할 것. 이렇게 비밀번호 폼 따로 설정하면 비번이 안보임.
        # + input box에 placeholder 적용 위해 widgets 사용.
        widgets = {
            'email': django_forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'name': django_forms.TextInput(attrs={'placeholder': '성명'}),
            'username': django_forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': django_forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }

    # 해시 알고리즘을 적용하는 코드.
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
