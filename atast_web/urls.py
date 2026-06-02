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
    path('photocontest',views.photocontest,name='photocontest'),
    path('ai',views.ai,name='ai'),
    path('genius',views.genius,name='genius'),
    path('team',views.team,name='team'),
    path('btech',views.btech,name='btech'),
    path('sss', views.sss, name='sss'),
    path('news', views.news, name='news'),
    path('oro_poussins', views.oro_poussins, name='oro_poussins'),
    path('oro_juniors', views.oro_juniors, name='oro_juniors'),
    path('oro_colleges', views.oro_colleges, name='oro_colleges'),
    path('oro_seniors', views.oro_seniors, name='oro_seniors'),
    path('oro_comp_bowling', views.oro_comp_bowling, name='oro_comp_bowling'),
    path('oro_comp_robofoot', views.oro_comp_robofoot, name='oro_comp_robofoot'),
    path('oro_comp_smartcity', views.oro_comp_smartcity, name='oro_comp_smartcity'),
    path('oro_comp_linefollower', views.oro_comp_linefollower, name='oro_comp_linefollower'),
    path('oro_comp_sumo', views.oro_comp_sumo, name='oro_comp_sumo'),
    path('oro_comp_roborace', views.oro_comp_roborace, name='oro_comp_roborace'),
    path('oro_comp_maze', views.oro_comp_maze, name='oro_comp_maze'),
    path('oro_comp_coding', views.oro_comp_coding, name='oro_comp_coding'),
    path('oro_comp_firefighting', views.oro_comp_firefighting, name='oro_comp_firefighting'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
