from django.urls import path
from cms_app import views

app_name = 'cms_app'

urlpatterns = [
    path('',views.index, name='index'),
    path('post/<int:id>', views.post, name = 'user_post'),
    path('register/', views.register, name ='register'),
    path('login/', views.user_login, name ='user_login'),
    path('sort/<str:by>/<int:id>', views.post_sort, name ='post_sort'),



    path('admin_home/', views.admin_index, name = "admin_index"),
    path('admin_home/category/', views.admin_category, name = 'category'),
    path('admin_home/category/delete/<int:id>', views.cat_delete, name = 'cat_delete'),
    path('admin_home/category/edit/<int:id>', views.cat_edit, name = 'cat_edit'),
    path('admin_home/post/', views.admin_post, name='post'),
    path('admin_home/post/delete/<int:id>', views.post_delete, name='post_delete'),
    path('admin_home/post/edit/<int:id>', views.post_edit, name='post_edit'),
    path('admin_home/post/add/', views.post_add, name='post_add'),
    path('admin_home/comments/', views.comment, name='comment'),
    path('admin_home/comments/<int:id>', views.comment_delete, name='comment_delete'),
    path('admin_home/comments/<int:id>/<str:status>', views.comment_approval, name='comment_approval'),
    path('admin_home/users/', views.users, name ='SeeUsers'),
    path('admin_home/users/add/', views.user_add, name ='user_add'),
    path('admin_home/users/<int:id>/role/<int:isAdmin>/', views.user_role, name ='user_role'),
    path('admin_home/users/<int:id>/delete', views.user_delete, name ='user_delete'),
    path('admin_home/user_profile/', views.user_profile, name ='user_profile'),
    path('admin_home/logout/', views.user_logout, name ='user_logout'),


]
