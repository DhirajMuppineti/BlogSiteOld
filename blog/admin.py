from django.contrib import admin
from .models import Comment,Blog,LikedPost

# Register your models here
admin.site.register(Comment)
admin.site.register(Blog)
admin.site.register(LikedPost)
