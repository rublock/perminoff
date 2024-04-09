from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Посты, административный раздел
    list_display - отображаемые на странице
    list_filter - позволяет фильтровать результаты по полям
    search_fields - строка поиска
    prepopulated_fields - навигационные ссылки для навигации по иерархии дат
    raw_id_fields - поисковый виджет
    date_hierarchy - строки поиска находятся навигационные ссылки для навигации по иерархии дат
    ordering - сортировка
    """

    list_display = ["title", "id", "author", "publish", "status"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Комментарии к статьям, административный раздел"""

    list_display = ["name", "email", "post", "created", "active"]
    list_filter = ["active", "created", "updated"]
    search_fields = ["name", "email", "body"]
