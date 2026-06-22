from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('oro', views.oro_home, name='oro_home'),

    # ORO category pages
    path('oro_poussins', views.oro_poussins, name='oro_poussins'),
    path('oro_juniors', views.oro_juniors, name='oro_juniors'),
    path('oro_colleges', views.oro_colleges, name='oro_colleges'),
    path('oro_seniors', views.oro_seniors, name='oro_seniors'),

    # ORO competitions - Poussins
    path('oro_poussins_bowling', views.oro_poussins_bowling, name='oro_poussins_bowling'),
    path('oro_poussins_robofoot', views.oro_poussins_robofoot, name='oro_poussins_robofoot'),
    path('oro_poussins_smartcity', views.oro_poussins_smartcity, name='oro_poussins_smartcity'),

    # ORO competitions - Juniors
    path('oro_juniors_bowling', views.oro_juniors_bowling, name='oro_juniors_bowling'),
    path('oro_juniors_robofoot', views.oro_juniors_robofoot, name='oro_juniors_robofoot'),
    path('oro_juniors_smartcity', views.oro_juniors_smartcity, name='oro_juniors_smartcity'),

    # ORO competitions - Colleges
    path('oro_colleges_linefollower', views.oro_colleges_linefollower, name='oro_colleges_linefollower'),
    path('oro_colleges_smartcity', views.oro_colleges_smartcity, name='oro_colleges_smartcity'),
    path('oro_colleges_sumo', views.oro_colleges_sumo, name='oro_colleges_sumo'),
    path('oro_colleges_roborace', views.oro_colleges_roborace, name='oro_colleges_roborace'),
    path('oro_colleges_robofoot', views.oro_colleges_robofoot, name='oro_colleges_robofoot'),
    path('oro_colleges_maze', views.oro_colleges_maze, name='oro_colleges_maze'),
    path('oro_colleges_firefighting', views.oro_colleges_firefighting, name='oro_colleges_firefighting'),

    # ORO competitions - Seniors
    path('oro_seniors_linefollower', views.oro_seniors_linefollower, name='oro_seniors_linefollower'),
    path('oro_seniors_smartcity', views.oro_seniors_smartcity, name='oro_seniors_smartcity'),
    path('oro_seniors_sumo', views.oro_seniors_sumo, name='oro_seniors_sumo'),
    path('oro_seniors_coding', views.oro_seniors_coding, name='oro_seniors_coding'),
    path('oro_seniors_coding/grade', views.oro_seniors_coding_grade, name='oro_seniors_coding_grade'),
    path('oro_seniors_roborace', views.oro_seniors_roborace, name='oro_seniors_roborace'),
    path('oro_seniors_maze', views.oro_seniors_maze, name='oro_seniors_maze'),
    path('oro_seniors_firefighting', views.oro_seniors_firefighting, name='oro_seniors_firefighting'),

    path('dashboard', views.oro_dashboard, name='oro_dashboard'),
    path('dashboard/login', views.oro_dashboard_login, name='oro_dashboard_login'),
    path('dashboard/release-coding-grader', views.oro_release_coding_grader, name='oro_release_coding_grader'),
    path('dashboard/logout', views.oro_dashboard_logout, name='oro_dashboard_logout'),
    path('dashboard/data', views.oro_dashboard_data, name='oro_dashboard_data'),
    path('dashboard/score', views.score_update, name='oro_score_update'),
    path('dashboard/team', views.team_add, name='oro_team_add'),
    path('dashboard/team/update', views.team_update, name='oro_team_update'),

    path('registration', views.registration, name='oro_registration'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
