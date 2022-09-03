from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import PostsForm, CommentForm
from .models import Post, Comment, Category
from django.db.models import F


# Create your views here.

class BlogView(ListView):
    template_name = "blog.html"
    model = Post
    context_object_name = 'all_posts'
    paginate_by = 10
class Search(ListView):
    template_name = 'blog.html'
    context_object_name = 'posts_search'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s = {self.request.GET.get('s')} &"
        return context


# class CreateView(TemplateView):
#     template_name = "create.html"


# def create_post(request):
#     if request.method == 'POST':
#         form = PostsForm(request.POST)
#         if form.is_valid() and request.user.is_authenticated:
#             # author = Post.objects.create(author=request.user)
#             # print(author)
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('details')
#         else:
#             messages.error(request, 'Ошибка создания')
#     else:
#         form = PostsForm()
#     return render(request, 'create.html', {'form': form})
class CreatePost(LoginRequiredMixin, CreateView):
    login_url = 'login'
    model = Post
    template_name = 'create.html'
    form_class = PostsForm

    def form_valid(self, form):
        if form.is_valid() and self.request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = self.request.user

            post.save()
        else:
            messages.error(self.request, 'Ошибка создания')

        return super().form_valid(form)


class ViewPosts(FormMixin, DetailView):
    model = Post
    context_object_name = 'posts_item'
    template_name = 'details.html'
    form_class = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        return context

    def post(self, request, *args, **kwargs):

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):

        post = Post.objects.get(slug=self.kwargs['slug'])

        comment = Comment(
            body=form.cleaned_data["body"],
            post=post
        )

        comment.author = self.request.user

        comment.save()
        return HttpResponseRedirect(self.request.path_info)
