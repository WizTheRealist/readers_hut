from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Count
from .models import Post, Category, Newsletter
from .forms import NewsletterForm, ContactForm

def home(request):
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:3]
    recent_posts = Post.objects.filter(status='published')[:6]
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    
    context = {
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)

def post_list(request):
    posts = Post.objects.filter(status='published')
    
    # Search
    search_query = request.GET.get('q', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'search_query': search_query,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    
    related_posts = Post.objects.filter(
        status='published',
        category=post.category
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category)
    
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, slug):
    posts = Post.objects.filter(status='published', tags__slug=slug)
    
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': slug,
        'posts': posts,
    }
    return render(request, 'blog/tag_posts.html', context)

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('blog:contact')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'blog/contact.html', context)

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            messages.error(request, 'Invalid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'blog:home'))