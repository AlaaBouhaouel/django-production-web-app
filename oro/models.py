from django.db import models

# Create your models here.

ORO_COMPS = [
    ("bowling", "Bowling"),
    ("line_follower", "Line Follower"),
    ("robofoot", "RoboFoot"),
    ("smart_city", "Smart City"),
    ("maze", "Maze"),
    ("sumo", "Sumo"),
    ("roborace", "RoboRace"),
    ("firefighting", "Firefighting"),
    ("coding_mission", "Coding Mission"),
]

ORO_AGE_CAT = [
    ("poussins", "Poussins"),
    ("juniors", "Juniors"),
    ("colleges", "Colleges"),
    ("seniors", "Seniors"),
]

class Registration(models.Model):

    COMPETITION_CHOICES = [
    ('genius', 'Genius Olympiad'),
    ('robotex', 'Robotex'),
    ('ifest', 'iFest'),
    ('vex', 'VEX'),
    ('castic', 'CASTIC'),
    ('jwp', 'Junior Water Prize'),
    ('ioai', 'IOAI')
        ]
    
    CATEGORIES = [
    ('engineering', 'Engineering'),
    ('energy', 'Energy'),
    ('env', 'Environment'),
    ('art', 'Arts & Humanities'),
    ('software', 'Softwares & AI'),
    ('physics', 'Physics'),
    ('chemistry', 'Chemistry')
        ]
    CLUBS = [
    ('sousse', 'Sousse'),
    ('monastir', 'Monastir'),
    ('moknine', 'Moknine'),
    ('ksarhlel', 'Ksar Hellel'),

        ]
    
    ORO_COMPS = ORO_COMPS
    ORO_AGE_CAT = ORO_AGE_CAT
    
    competition = models.CharField(max_length=50, choices=COMPETITION_CHOICES, blank=True)
    name = models.CharField(max_length=100)
    mail = models.EmailField()
    age = models.PositiveIntegerField()
    atastian = models.BooleanField(default=False)
    club = models.CharField(choices=CLUBS, blank=True)
    city = models.CharField(max_length=40)
    team = models.BooleanField(default=False)
    teammates = models.TextField(blank=True)
    categorie = models.CharField(max_length=50, choices=CATEGORIES, blank=True)
    project_title = models.CharField(max_length=50, blank=True)
    project_desc = models.TextField(blank=True)





class teams(models.Model):
    team_name = models.CharField(max_length=255, blank = False)
    team_members_number = models.PositiveIntegerField(blank = False)
    competition = models.CharField(max_length=30, choices=ORO_COMPS)
    category = models.CharField(max_length=20, choices=ORO_AGE_CAT)

    score = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(blank=True, null=True)
    

    class Meta:
        ordering = ['rank']


class OROSystemSettings(models.Model):
    coding_grader_released = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={"coding_grader_released": False})
        return obj


