from django.urls import path
from django.conf.urls import url
from .views import *

app_name = 'app'

urlpatterns = [
            path('', MainListView.as_view(), name='index'),
            path('section/<int:pk>/', section, name='section'),
            path('post/<int:pk>/', post, name='post'),
            path('search/', search, name='search'),
            path('post/<int:pk>/update/', update_post, name='update-post'),
            path('post/<int:pk>/delete/', delete_post, name='delete-post'),
            path('comment/<int:pk>/update/', update_comment, name='update-comment'),
            path('comment/<int:pk>/delete/', delete_comment, name='delete-comment'),
            path('post/comment/<int:pk>/', response, name='comment'),
            path('cancel/', cancel, name='cancel'),

]