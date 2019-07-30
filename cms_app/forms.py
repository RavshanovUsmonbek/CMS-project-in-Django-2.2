from django import forms
from cms_app.models import UserProfile, Comment, Catagory, Post
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields =['cat_title',]
        widgets = {'cat_title':forms.TextInput(attrs={'class':'form-control','name':'cat_title',})}

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['post_id', 'post_date', 'post_comment_count']

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude =['post_id',]

class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username', 'email', 'first_name', 'last_name', 'password']
        widgets ={'password':forms.PasswordInput()}

class RegisterUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_image','user_isAdmin']

class EditUserProfile(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_image',]

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ['com_content']
