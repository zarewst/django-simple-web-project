from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages

from .forms import *
from .models import Category, Article
from datetime import datetime


# Create your views here.


# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'title': 'Jutsu',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'JUTSU'
    }


# def category_view(request, pk):
#     articles = Article.objects.filter(category_id=pk)
#     category = Category.objects.get(pk=pk)
#     context = {
#         'title': f'Категория: {category.title}',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)


class ArticleListByCategory(ArticleListView):

    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['pk'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context


def article_view(request, pk, new_context=None):
    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=article)

    article.views += 1
    article.save()

    comment_form = CommentForm()

    context = {
        'comment_form': comment_form,
        'comments': comments,
        'article': article
    }

    try:
        context['profile'] = Profile.objects.get(user_id=request.user.pk)
        context.update(new_context)

    except:
        pass

    context['message'] = 'Чтобы оставить комментарий войдите в аккаунт или зарегистрируйтесь'

    return render(request, 'blog/article_detail.html', context)


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()
        context['title'] = f'Статья: {article.title}'

        context['comment_form'] = CommentForm()

        context['comments'] = Comment.objects.filter(article=article)

        try:
            context['profile'] = Profile.objects.get(user_id=self.request.user.pk)

        except:
            pass

        context['message'] = 'Чтобы оставить комментарий войдите в аккаунт или зарегистрируйтесь'

        return context


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             article = Article.objects.create(**form.cleaned_data)
#             article.save()
#             return redirect('article', article.pk)
#
#     else:
#         form = ArticleForm()
#
#     context = {
#         'form': form,
#         'title': 'Создание статьи'
#     }
#
#     return render(request, 'blog/add_article.html', context)


class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/add_article.html'
    extra_context = {
        'title': 'Создание статьи'
    }


class ArticleUpdate(UpdateView):
    model = Article
    context_object_name = 'article'
    form_class = ArticleForm
    template_name = 'blog/add_article.html'


class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'Добро пожаловать')
                return redirect('index')
            else:
                messages.warning(request, 'Неверный логин или пароль')
                return redirect('login')

        else:
            messages.warning(request, 'Неверный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Войти в аккаунт',
        'form': form
    }
    return render(request, 'blog/login.html', context)


def user_logout(request):
    logout(request)
    messages.warning(request, 'Успешно вышли')
    return redirect('index')


class SearchResults(ArticleListView):
    def get_queryset(self):
        word = self.request.GET.get('q').capitalize()
        articles = Article.objects.filter(title__icontains=word)
        return articles


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            form2 = ProfileForm(request.POST, request.FILES)
            if form2.is_valid():
                profile = form2.save(commit=False)
                profile.user = user
                profile.status_id = 2
                profile.rank_id = 13
                profile.save()

                messages.success(request, 'Регистрация прошла упешно. Войдите в аккаунт')
                return redirect('login')

        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
                return redirect('register')

    else:
        form = RegistrationForm()
        form2 = ProfileForm()

    context = {
        'title': 'Регистрация',
        'form': form,
        'form2': form2
    }

    return render(request, 'blog/register.html', context)


def save_comment(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)

        comment.article = Article.objects.get(pk=pk)
        comment.profile = Profile.objects.get(user_id=request.user.id)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий опубликован')
        return redirect('article', pk)


def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    comment.delete()
    messages.success(request, 'Комментарий был удален')

    return redirect('article', comment.article.pk)


# class UpdateComment(UpdateView):
#     model = Comment
#     context_object_name = 'comment'
#     template_name = 'blog/article_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         comment = Comment.objects.get(pk=self.kwargs['pk'])
#         form = UpdateCommentForm()
#         form.Meta.widgets['text'] = comment.text
#         form.save()
#         context['form'] = form
#         return context


def edit_comment(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    form = UpdateCommentForm(instance=comment)

    pk = article_id

    context = {
        'comment_form': form
    }

    messages.warning(request, 'Изменение комментарий ⤵')

    return article_view(request, pk=pk, new_context=context)


def save_edited_comment(request, pk):
    comment = Comment.objects.get(pk=pk)

    form = CommentForm(request.POST)
    if form.is_valid():
        comment1 = form.save()

        comment1.user = request.user
        comment1.article = Article.objects.get(pk=comment.article.pk)
        comment1.created_at = comment.created_at
        comment1.profile = Profile.objects.get(user_id=request.user.id)
        comment1.save()

    comment.delete()
    messages.success(request, 'Комментарий изменён')

    return redirect('article', comment.article.pk)


def profile_view(request, pk):
    profile = Profile.objects.get(user_id=pk)

    # try:
    #     if profile.created_at is not None:
    #         data = profile.created_at.date()
    #         the_date = str(data.strftime('%Y-%m-%d'))
    #         now = str(datetime.now())
    #         if int(now.split('-')[0]) - int(the_date.split('-')[0]) >= 1:
    #             profile.rank_id += 1
    #             profile.save()
    # except:
    #     pass

    context = {
        'profile': profile,
        'title': f'Пользователь: {profile.user.username}'
    }

    return render(request, 'blog/profile.html', context=context)


def about_site(request):
    context = {
        'title': 'О сайте'
    }

    return render(request, 'blog/about_site.html', context)
