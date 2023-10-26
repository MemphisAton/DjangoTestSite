from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from women.forms import AddPostForm
from .models import Women, TagPost
from .utils import DataMixin


# def index(request):
#     posts = Women.published.all().select_related('cat')  # загружаем все связанные данные из таблицы категории
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = 'women/index.html'  # информауия в html будет идти через object_list либо определить context_object_name
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):  # что будет отображаться в качестве списка
        return Women.published.all().select_related('cat')

    # template_name = 'women/index.html'
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts': Women.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }
    # на будущее
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context


# def handle_uploaded_file(f):  # сохранение файла методом чанкс по определенному маршруту
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
@login_required  # доступ только для авторизованных ()-можно тут прописать куда перенаправлять login_url = , или в сеттингс
def about(request):
    contact_list = Women.published.all()  # какие элементы используем
    paginator = Paginator(contact_list, 3)  # класс пагинатора (список , количество для разбивки)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # получаем текущую страницу
    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1, }
#     return render(request, 'women/post.html', data)


class ShowPost(DataMixin, DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # переменная из маршрута
    context_object_name = 'post'  # переменная откуда берется информация (стандарт: 'object')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request): # заменили на класс
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


# class AddPage(View):
#     def get(self, request):
#         form = AddPostForm()
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    # model = Women
    # fields = ['title', 'slug', 'content'] # '__all__' отображение всех полей название из модели
    template_name = 'women/addpage.html'
    # success_url = reverse_lazy('home')  # возвразает маршрут главной страницы,
    # если без то перенаправление берется из метода get_absolute_url
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women'

    # разрешение которым должен обладать пользователь для доступа к странице
    # (имя приложения.add_имя таблицы с которым связано разрешение)(<приложение>.<действие>_<таблица>)

    # login_url = 'users:login' #куда послать если нет авторизации
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Редактирование статьи',
    # }
    permission_required = 'women.change_women'
    # разрешение которым должен обладать пользователь для доступа к странице
    # (имя приложения.add_имя таблицы с которым связано разрешение)(<приложение>.<действие>_<таблица>)


class DeletePage(DeleteView):
    model = Women
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')


@permission_required(perm='women.view_women', raise_exception=True)  # декоратор на разрешение функции
def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat')
#
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'women/index.html', context=data)


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False  # при пустом списке генерируется исключение 404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id,
                                      )

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {
#         'title': f"Тег: {tag.tag}",
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None
#     }
#     return render(request, 'women/index.html', context=data)


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
