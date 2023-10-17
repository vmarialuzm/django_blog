from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, View
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CreatePost(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, 'La publicación se ha creado con éxito')
        return redirect('index')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, completa todos los campos requeridos')
        return super().form_invalid(form)

class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)

class PostDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.all()
        form = CommentForm()
        return render(request, "blog/post_details.html", {'post': post, 'comments': comments, 'form': form})
    
    def post(self, request, id):
        form = CommentForm(request.POST)
        print("1")
        if form.is_valid():
            form.instance.user = request.user
            print("2")
            form.instance.post_id = id
            form.save()
            messages.success(self.request, 'El comentario se ha creado con éxito')
            print("5")
        else:
            print("3")
            messages.error(self.request, 'Por favor, completa todos los campos requeridos')
        print("4")
        return redirect('post_details', id=id)

