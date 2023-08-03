from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .models import *


class PostList(ListView):
    model = Post
    ordering = '-date_post'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsList(PostList):
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(category_type='NW')
        return queryset


class ArticleList(PostList):
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(category_type='AR')
        return queryset
class PostDetail(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post_detail'


class AuthorList(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'news/authors.html'


class SearchList(ListView):
    model = Post
    ordering = '-date_post'
    context_object_name = 'search'
    template_name = 'news/search_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'AR'
        return super().form_valid(form)


class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.category_type = 'NW'
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)





