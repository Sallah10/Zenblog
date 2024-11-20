from django.shortcuts import render
from typing import Any, Optional
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ContactForm
from .forms import PostForm



# def home(request):
#     context = {
#         'posts': Post.objects.all
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    # fields = ['title','content']
    template_name = 'blog/post_create.html'
    success_url = '/home/'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
            post = self.get_object()
            if self.request.user == post.author:
                return True
            return False
       
# def home(request):
#     return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

def category(request):
    return render(request, 'blog/category.html')

def contact(request):
    return render(request, 'blog/contact.html')

def search_result(request):
    return render(request, 'blog/search-result.html')

def single_post(request):
    return render(request, 'blog/single-post.html')

# contact page 
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data, such as sending an email
            # You can access form fields using form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            # subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # Example: send email
            # You would need to implement email sending logic here
            # ...

            # Return a success message or redirect
            return render(request, 'blog/contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})
