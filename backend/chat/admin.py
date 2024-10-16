from django.contrib import admin

from chat.models import ChatRoom


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "language", "level", "situation"]
    list_filter = ["language", "level"]
    search_fields = ["title", "situation", "my_role", "gpt_role"]
    readonly_fields = ["user"]

    fieldsets = (
        (None, {"fields": ("user", "title", "language", "level")}),
        ("Situation", {"fields": ("situation",)}),
        (
            "Roles",
            {
                "fields": (
                    "my_role",
                    "gpt_role",
                )
            },
        ),
    )


admin.site.register(ChatRoom, ChatRoomAdmin)
