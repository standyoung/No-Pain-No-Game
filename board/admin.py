from django.contrib import admin
from board.models import *

# Register your models here.


class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('p_type',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'post_date', 'postname', 'p_type',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'post_id', 'comment_date',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostType, PostTypeAdmin)