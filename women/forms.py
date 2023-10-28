from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Husband, Women


# @deconstructible
# class RussianValidator:  # пишем свой собственный валидатор
#     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
#     code = 'russian'
#
#     def __init__(self, message=None):
#         self.message = message if message else "кирилл и мефодий для кого старались?"
#
#     def __call__(self, value, *args, **kwargs):
#         if not (set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.ModelForm):
    # title = forms.CharField(
    #     max_length=255,
    #     label="Заголовок",
    #     min_length=5,# min_length минимальная длина
    #     widget=forms.TextInput(attrs={'class': 'form-input'}),
    #     error_messages={
    #         'min_length': "умный слишком?",
    #         'required': 'да напиши ты заголовок'}
    # )
    # slug = forms.SlugField(
    #     max_length=255,
    #     label='url',
    #     validators=[MinLengthValidator(5, message='да блин')]
    # )
    # content = forms.CharField(
    #     widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}),
    #     required=False, # required обязательность поля
    #     label='Контент'
    # )
    # is_published = forms.BooleanField(
    #     required=False,
    #     initial=True,     # initial галка стоит автоматически
    #     label='Статус'
    # )
    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Категория не выбрана'  # окно выбора
    )
    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        label='Муж',
        required=False,
        empty_label='не замужем'  # окно выбора
    )

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'husband',
                  'tags']  # указывать названия из модели
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }
        labels = {'slug': 'URL'}  # смена названий в форме

    # def clean_title(self):  # тоже создали валидатор
    #     title = self.cleaned_data['title']
    #     ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    #     if not (set(title) <= set(ALLOWED_CHARS)):
    #         raise ValidationError("кирилл и мефодий для кого старались?")
    # создаем валидатор
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")  # к ImageField надо установить pillow


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
