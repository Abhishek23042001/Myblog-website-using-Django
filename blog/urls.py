from django.urls import path, include
from .import views

urlpatterns = [
    path('postComment',views.postComment,name="postComment"),# put it at the top so that blog/slug doesn't mached when comments are posted
    path('',views.blogHome,name='blogHome'),
    path('<int:sno>',views.blogPost,name='blogPost'), #<str:slug>
]
