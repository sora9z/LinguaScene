from django.contrib import admin

from chat.models import ChatRoom

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'language', 'level', 'situation'] 
    list_filter = ['language', 'level'] 
    search_fields = ['title', 'situation', 'my_role', 'gpt_role']
    readonly_fields = ['user']

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'language', 'level')
        }),
        ('Situation', {
            'fields': ('situation', 'situation_en')
        }),
        ('Roles', {
            'fields': ('my_role', 'my_role_en', 'gpt_role', 'gpt_role_en')
        }),
    )

admin.site.register(ChatRoom, ChatRoomAdmin)
    

    

