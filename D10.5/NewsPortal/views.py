from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Category, Author, Post, PostCategory, Comment, Subscribers
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from .tasks import email_add_post, monday_8am
from datetime import datetime, timedelta
 
class PostList(ListView):
    model = Post
    template_name = 'news.html' 
    context_object_name = 'news' 
    queryset = Post.objects.order_by('-created')
    paginate_by = 2
    
    
    
class SearchList(ListView):
    model = Post
    template_name = 'search.html' 
    context_object_name = 'search' 
    queryset = Post.objects.order_by('-created')

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        
        return context


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('NewsPortal.change_post', )
    success_url = '/search/'
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id) 



class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    context_object_name = 'news'
    success_url = '/search/' 
    permission_required = ('NewsPortal.delete_post', )
 

class AddList(PermissionRequiredMixin, ListView):
    model = Post
    template_name = 'add.html' 
    context_object_name = 'add' 
    queryset = Post.objects.order_by('-created')
    form_class = PostForm
    permission_required = ('NewsPortal.add_post', )
    

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['form'] = PostForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            
            title = request.POST['title']
            text = request.POST['text']
            email = subscribers_list(request.POST['cats'])
            email_add_post.delay(title, text, email)
            form.save() 
            
        return super().get(request, *args, **kwargs)       

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html' 
    context_object_name = 'news'  

class AddSubscribers( LoginRequiredMixin, TemplateView):
    model = Post
    template_name = 'subscribers.html'
    
    def get_context_data(self,**kwargs):
        user_id = self.request.user.pk                
        category = PostCategory.objects.filter(post_id = self.kwargs.get('pk'))
        for cat in category:
            if not Subscribers.objects.filter(user_id = user_id, cats_id = cat.category_id):
                Subscribers.objects.create(user_id = user_id, cats_id = cat.category_id)


def subscribers_list(categorys):
    email_list = []   
    for category in categorys:
        cats = Subscribers.objects.filter(cats_id = category)
        for user in cats:
            emails = User.objects.filter(id=user.user_id)
            for email in emails:
                email_list.append(email.email )
    return email_list