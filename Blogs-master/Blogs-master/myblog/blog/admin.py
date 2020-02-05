from django.contrib import admin
from .models import Post,Comment,Reply

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish',
                       'status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

class CommentAdmin(admin.ModelAdmin):
    list_disply =('comment_post','comment_user','comments','created_on')
    list_filter =('comments','comment_user')
    search_fields=('comments',)
    ordering=['created_on']

class ReplyAdmin(admin.ModelAdmin):
    list_disply=('comment_posts','reply_user','reply','created_on')
    list_filter=('created_on','reply')
    ordering=['created_on']


admin.site.register(Reply, ReplyAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
