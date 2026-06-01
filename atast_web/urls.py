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

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
