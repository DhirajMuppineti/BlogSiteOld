from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import template

register = template.Library()

def like_blog(request,pk):
    if request.method == "GET":
        liked_post = LikedPost(user = request.user,blog = Blog.objects.get(pk=pk))
        liked_post.save()
    return redirect('blog:read_blog',pk)
        

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("blog:main")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="blog/register.html", context={"register_form":form})

# Create your views here.
class BaseView(View):
    def get(self, request):
        return render(request, 'blog/index.html')


  
class MainView(LoginRequiredMixin,View):  
    def get(self, request):
        blogs = Blog.objects.all().order_by('likes')[:10][::-1]
        ctx = {"blogs" : blogs}
        
        return render(request, 'blog/main.html',ctx)

    
class BlogRead(LoginRequiredMixin,View):
    def get(self,request,pk):
        blog = Blog.objects.get(pk=pk)
        comments = Comment.objects.filter(blog = blog)
        ctx = {"blog":blog,"comments":comments}
        return render(request,'blog/read.html',ctx)
        
 
    
class BlogCreate(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title','content']
    success_url = reverse_lazy('blog:main')
    
    def form_valid(self, form):
        author = self.request.user
        form.instance.author = author
        return super(BlogCreate, self).form_valid(form)


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title','content']
    success_url = reverse_lazy('blog:main')


class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    fields = '__all__'
    success_url = reverse_lazy('blog:main')
    
class CommentBlog(LoginRequiredMixin,View):
    def post(self,request,pk):
        blog = Blog.objects.get(pk=pk)
        comment_text = request.POST['comment']
        comment = Comment(user = request.user,comment = comment_text,blog = blog)
        comment.save()
        next = request.POST.get('next', '/')
        return redirect(next)   