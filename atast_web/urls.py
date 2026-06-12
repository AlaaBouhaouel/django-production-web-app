from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('gifts', views.index_store, name='gifts'),
    path('ifest', views.ifest, name='ifest'),
    path('maker_space', views.maker_space, name='maker_space'),
    path('xminds', views.xminds, name='xminds'),
    path('clubs', views.clubs, name='clubs'),
    path('test', views.test, name='test'),
    path('spell', views.spell, name='spell'),
    path('tunibrico', views.tunibrico, name='tunibrico'),
    path('camp', views.camp, name='camp'),
    path('training', views.training, name='training'),
    path('cyber', views.cyber, name='cyber'),
    path('oro', views.oro, name='oro'),
    path('photocontest', views.photocontest, name='photocontest'),
    path('ai', views.ai, name='ai'),
    path('genius', views.genius, name='genius'),
    path('team', views.team, name='team'),
    path('btech', views.btech, name='btech'),
    path('sss', views.sss, name='sss'),
    path('news', views.news, name='news'),
    path('isef', views.isef, name='isef'),
    path('vex', views.vex, name='vex'),
    path('castic', views.castic, name='castic'),
    path('gwp', views.gwp, name='gwp'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),

    # ── ORO category pages ──
    path('oro_poussins', views.oro_poussins, name='oro_poussins'),
    path('oro_juniors', views.oro_juniors, name='oro_juniors'),
    path('oro_colleges', views.oro_colleges, name='oro_colleges'),
    path('oro_seniors', views.oro_seniors, name='oro_seniors'),

    # ── ORO competitions — Poussins ──
    path('oro_poussins_bowling', views.oro_poussins_bowling, name='oro_poussins_bowling'),
    path('oro_poussins_robofoot', views.oro_poussins_robofoot, name='oro_poussins_robofoot'),
    path('oro_poussins_smartcity', views.oro_poussins_smartcity, name='oro_poussins_smartcity'),

    # ── ORO competitions — Juniors ──
    path('oro_juniors_bowling', views.oro_juniors_bowling, name='oro_juniors_bowling'),
    path('oro_juniors_robofoot', views.oro_juniors_robofoot, name='oro_juniors_robofoot'),
    path('oro_juniors_smartcity', views.oro_juniors_smartcity, name='oro_juniors_smartcity'),

    # ── ORO competitions — Colleges ──
    path('oro_colleges_linefollower', views.oro_colleges_linefollower, name='oro_colleges_linefollower'),
    path('oro_colleges_smartcity', views.oro_colleges_smartcity, name='oro_colleges_smartcity'),
    path('oro_colleges_sumo', views.oro_colleges_sumo, name='oro_colleges_sumo'),
    path('oro_colleges_roborace', views.oro_colleges_roborace, name='oro_colleges_roborace'),
    path('oro_colleges_robofoot', views.oro_colleges_robofoot, name='oro_colleges_robofoot'),
    path('oro_colleges_maze', views.oro_colleges_maze, name='oro_colleges_maze'),
    path('oro_colleges_firefighting', views.oro_colleges_firefighting, name='oro_colleges_firefighting'),

    # ── ORO competitions — Seniors ──
    path('oro_seniors_linefollower', views.oro_seniors_linefollower, name='oro_seniors_linefollower'),
    path('oro_seniors_smartcity', views.oro_seniors_smartcity, name='oro_seniors_smartcity'),
    path('oro_seniors_sumo', views.oro_seniors_sumo, name='oro_seniors_sumo'),
    path('oro_seniors_coding', views.oro_seniors_coding, name='oro_seniors_coding'),
    path('oro_seniors_roborace', views.oro_seniors_roborace, name='oro_seniors_roborace'),
    path('oro_seniors_maze', views.oro_seniors_maze, name='oro_seniors_maze'),
    path('oro_seniors_firefighting', views.oro_seniors_firefighting, name='oro_seniors_firefighting'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
