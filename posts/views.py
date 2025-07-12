from django.shortcuts import render
from .models import Category,News


def index(request):
    categories = Category.objects.all()
    first_news = []
    for category in categories:
        category_first_post = News.objects.filter(category=category).order_by('-created_at').first()
        if category_first_post is not None:
            first_news.append(category_first_post)
    if len(first_news) < 4:
        news = News.objects.all()
        first_news.extend(news[len(news)-4:len(news)-len(first_news)])

    news = News.objects.all().order_by('-id')


    return render(request, 'index.html', {'categories':categories, 'first_news':first_news, 'news':news})
