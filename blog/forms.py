from django import forms
from .models import Post, Comment, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'category', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug']