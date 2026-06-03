from django.shortcuts import render
from .models import NewsArticle

def index(request):
    return render(request, 'index.html')

def index_store(request):
    return render(request, 'index_store.html')

def ifest(request):
    return render(request, 'ifest.html')

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



# ── ORO category pages ──
def oro_poussins(request):
    return render(request, 'oro_poussins.html')

def oro_juniors(request):
    return render(request, 'oro_juniors.html')

def oro_colleges(request):
    return render(request, 'oro_colleges.html')

def oro_seniors(request):
    return render(request, 'oro_seniors.html')

# ── ORO competition pages — Poussins ──
def oro_poussins_bowling(request):
    return render(request, 'oro_poussins_bowling.html')

def oro_poussins_robofoot(request):
    return render(request, 'oro_poussins_robofoot.html')

def oro_poussins_smartcity(request):
    return render(request, 'oro_poussins_smartcity.html')

# ── ORO competition pages — Juniors ──
def oro_juniors_bowling(request):
    return render(request, 'oro_juniors_bowling.html')

def oro_juniors_robofoot(request):
    return render(request, 'oro_juniors_robofoot.html')

def oro_juniors_smartcity(request):
    return render(request, 'oro_juniors_smartcity.html')

# ── ORO competition pages — Colleges ──
def oro_colleges_linefollower(request):
    return render(request, 'oro_colleges_linefollower.html')

def oro_colleges_smartcity(request):
    return render(request, 'oro_colleges_smartcity.html')

def oro_colleges_sumo(request):
    return render(request, 'oro_colleges_sumo.html')

def oro_colleges_roborace(request):
    return render(request, 'oro_colleges_roborace.html')

def oro_colleges_robofoot(request):
    return render(request, 'oro_colleges_robofoot.html')

def oro_colleges_maze(request):
    return render(request, 'oro_colleges_maze.html')

def oro_colleges_firefighting(request):
    return render(request, 'oro_colleges_firefighting.html')

# ── ORO competition pages — Seniors ──
def oro_seniors_linefollower(request):
    return render(request, 'oro_seniors_linefollower.html')

def oro_seniors_smartcity(request):
    return render(request, 'oro_seniors_smartcity.html')

def oro_seniors_sumo(request):
    return render(request, 'oro_seniors_sumo.html')

def oro_seniors_coding(request):
    return render(request, 'oro_seniors_coding.html')

def oro_seniors_roborace(request):
    return render(request, 'oro_seniors_roborace.html')

def oro_seniors_maze(request):
    return render(request, 'oro_seniors_maze.html')

def oro_seniors_firefighting(request):
    return render(request, 'oro_seniors_firefighting.html')
