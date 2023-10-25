from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255,
                             verbose_name='заголовок')
    slug = models.SlugField(max_length=255,
                            unique=True,
                            db_index=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",
                              default=None,
                              blank=True,
                              null=True,
                              verbose_name="Фото")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       # костыль для преобразования 0,1 в значения Bool, для вывода в таблицу админки
                                       default=Status.DRAFT)
    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT,
                            related_name='posts')
    tags = models.ManyToManyField('TagPost',
                                  blank=True,
                                  related_name='tags')
    husband = models.OneToOneField('Husband',
                                   on_delete=models.SET_NULL,
                                   blank=True, null=True,
                                   related_name='woman')
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               related_name='posts',
                               null=True,
                               default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Famous women'  # название таблицы в админке
        verbose_name_plural = 'Famous women'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):  # так же в админке добавляет кнопку 'СМОТРЕТЬ НА САЙТЕ'
        return reverse('post', kwargs={'post_slug': self.slug})

    # def save(self, *args, **kwargs):  # автоматическое создание слага при вызове метода save
    #     self.slug = slugify(translit_to_eng(self.title))
    #     super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category women'  # название таблицы в админке
        verbose_name_plural = 'Categories of women'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
