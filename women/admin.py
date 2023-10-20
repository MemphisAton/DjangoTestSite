from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Women, Category


class MarriedFilter(admin.SimpleListFilter):  # дополнительный пункт в фильтр
    title = 'статус'
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [('married', 'Замужем'),
                ('single', 'Свободна')]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'post_photo', 'photo', 'cat', 'husband',
              'tags', ]  # поля отображающиеся в админке при изменении записи
    # exclude = ['title', 'content']        # поля исключающиеся в админке при изменении записи
    readonly_fields = ['post_photo']  # поля для отображения но не редактирования
    list_display = ('post_photo', 'title', 'time_create', 'is_published', 'cat')  # отображение таблицы в админке
    list_display_links = ('title',)  # переход на обьект БД
    ordering = ('-time_create',)  # сортировка
    list_editable = ('is_published',)  # поля редактируемые в списке
    filter_horizontal = ('tags',)  # отображение списка
    prepopulated_fields = {'slug': ('title',)}  # поле надо обязательно сделать редактируемым
    list_per_page = 50  # максимальное количество отображения строк в таблице
    actions = ('set_published', 'set_draft',)  # добавляем действие над таблицей
    search_fields = ('title',
                     'cat__name',)  # добавляем строку поиска по таблице, через __ можно писать lookupы и категории, title__startswith(например)
    list_filter = (MarriedFilter, 'cat', 'is_published',)  # фильтрация по выбранным категориям
    save_on_top = True  # кнопки редактирования и снизу и сверху

    @admin.display(description="Изображение")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=30>")
        return "Без фото"

    @admin.action(description='Опубликовать выбранное')
    def set_published(self, request, queryset):  # создаем действие над таблицей
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f'Измененно {count} записей')  # создать всплывающее окно с текстом

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):  # создаем действие над таблицей
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f'{count} снято с публикации', messages.WARNING)  # изменим цвет записи


# admin.site.register(Women, WomenAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # отображение таблицы в админке
    list_display_links = ('id', 'name')  # переход на обьект БД
