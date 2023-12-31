from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, View, UpdateView, DeleteView
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

class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        if form.instance.user == self.request.user:
            form.save()
            messages.success(self.request, 'La publicación se ha editado con éxito') 
        else:
            messages.error(self.request, 'Sólo pueda editar el autor del post')
        return redirect('index')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Por favor, completa todos los campos requeridos')
        return super().form_invalid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('index')


class Index(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'blog/index.html', context)

class PostDetailView(View):

    def get(self, request, id):
        post = Post.objects.get(id=id)
        comments = Comment.objects.all()
        form = CommentForm()
        count_comments = len(Comment.objects.filter(post_id=post.id))
        context = {
            'post': post, 
            'comments': comments, 
            'form': form, 
            'count_comments': count_comments
        }
        return render(request, "blog/post_details.html", context)
    
    def post(self, request, id):
        form = CommentForm(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                form.instance.user = request.user
                form.instance.post_id = id
                form.save()
                messages.success(self.request, 'El comentario se ha creado con éxito')
            else:
                messages.error(self.request, 'Por favor, completa todos los campos requeridos')
        else:
            messages.error(self.request, "Debes logearte para realizar comentarios...")

        return redirect('post_details', id=id)


def update(request, id):
    print(request.user)
    if request.user.is_authenticated:
        comment = Comment.objects.get(id=id)
        if request.user.id == comment.user_id:
            form = CommentForm(request.POST or None, instance=comment)
            if form.is_valid():
                form.save()
                messages.success(request, "Comentario actualizado exitosamente!")
                return redirect('post_details', id=comment.post_id)
            return render(request, 'blog/post_details.html', {'form': form})
    return redirect('post_details', id=comment.post_id)   

def delete(request, id):
    if request.user.is_authenticated:
        deleted_it = Comment.objects.get(id=id)
        if request.user.id == deleted_it.user_id:
            deleted_it.delete()
            messages.success(request, "Comentario borrado exitosamente")
            return redirect('post_details', id=deleted_it.post_id)

def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
        post.disliked_by.remove(request.user)
    
    post.save()
    
    return redirect('index')

def disliked_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.disliked_by.all():
        post.disliked_by.remove(request.user)
    else:
        post.disliked_by.add(request.user)
        post.liked_by.remove(request.user)
    
    post.save()
    
    return redirect('index')


