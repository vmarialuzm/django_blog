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
        messages = Comment.objects.all()
        form = CommentForm()
        return render(request, "blog/post_details.html", {'post': post, 'messages': messages, 'form': form})
    
    def post(self, request, id):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.post_id = id
            form.save()
            messages.success(request, 'El comentario se ha creado con éxito')
        else:
            messages.error(request, 'Por favor, completa todos los campos requeridos')
        
        return redirect('post_details', id=id)


