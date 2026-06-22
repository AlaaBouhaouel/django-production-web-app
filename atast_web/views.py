from django.shortcuts import render
from .models import ifestImage, NewsArticle, LatestNews, Partners_Supporters, GalleryImage, Gifts

def index(request):
    latest_news = LatestNews.objects.all()[:4]
    partners_supporters = Partners_Supporters.objects.all()
    gallery_images = GalleryImage.objects.all()
    return render(request, 'index.html', {'latest_news': latest_news, 'partners_supporters': partners_supporters, 'gallery_images': gallery_images})

def index_store(request):
    gifts = Gifts.objects.all()
    return render(request, 'index_store.html', {'gifts': gifts})

def ifest(request):
    bg_image = ifestImage.objects.first()
    return render(request, 'ifest.html', {'bg_image': bg_image})

def maker_space(request):
    return render(request, 'maker_space.html')

def xminds(request):
    return render(request, 'xminds.html')

def clubs(request):
    return render(request, 'clubs.html')

def test(request):
    return render(request, 'test.html')

def genius(request):
    return render(request, 'genius.html')

def spell(request):
    return render(request, 'spell.html')

def ai(request):
    return render(request, 'ai.html')

def tunibrico(request):
    return render(request, 'tunibrico.html')

def camp(request):
    return render(request, 'camp.html')

def btech(request):
    return render(request, 'btech.html')

def isef(request):
    return render(request, 'isef.html')

def vex(request):
    return render(request, 'vex.html')

def castic(request):
    return render(request, 'castic.html')

def gwp(request):
    return render(request, 'gwp.html')

def robotex(request):
    return render(request, 'robotex.html')

def rc_china(request):
    return render(request, 'rc_china.html')

def training(request):
    return render(request, 'training.html')

def cyber(request):
    return render(request, 'cyber.html')

def oro(request):
    return render(request, 'oro.html')

def photocontest(request):
    return render(request, 'photocontest.html')

def team(request):
    return render(request, 'team.html')

def sss(request):
    return render(request, 'sss.html')



def news(request):
    featured = NewsArticle.objects.filter(is_featured=True).first()
    articles = NewsArticle.objects.filter(is_featured=False)
    return render(request, 'news.html', {'featured': featured, 'articles': articles})


def news_detail(request, news_id):
    article = LatestNews.objects.get(id=news_id)
    return render(request, 'news_detail.html', {'article': article})
