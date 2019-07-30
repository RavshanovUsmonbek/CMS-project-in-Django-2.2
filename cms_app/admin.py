from django.contrib import admin
from cms_app.models import Post, Comment, Catagory, UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Catagory)
