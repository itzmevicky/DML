from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(PostCount)
class PostcountAdmin(admin.ModelAdmin):
    list_display = ['id','like','dislike']

@admin.register(PostLikeBy)
class PostLikebyAdmin(admin.ModelAdmin):
    list_display = ['id','user','like','dislike']