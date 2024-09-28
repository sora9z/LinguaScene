from django.contrib import admin

from message.models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ['chat_room', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'chat_room__title']
    readonly_fields = ['chat_room', 'created_at']

    # 미리보기 재공 
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'    

admin.site.register(Message, MessageAdmin)