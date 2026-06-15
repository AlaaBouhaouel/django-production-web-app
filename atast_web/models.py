from django.utils import timezone
from django.db import models

# Create your models here.
class ifestImage(models.Model):
    image = models.ImageField(upload_to='ifest_bg/')

        
class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True, help_text='e.g. International · Competition')
    link = models.URLField(blank=True, null=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-published_date'] #So when you do NewsArticle.objects.all() in a view, you automatically get them newest-to-oldest

class Partners_Supporters(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    category = models.CharField(max_length=50, choices=[('partner', 'Partner'), ('supporter', 'Supporter')])
    website = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)  # For manual ordering of partners/supporters

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('this_year', 'This Year'),
        ('national', 'National'),
        ('international', 'International'),
        ('tunisia_team', 'Tunisia Team'),
    ]
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Image {self.id}"

    class Meta:
        ordering = ['-uploaded_at']


class LatestNews(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='latest_news/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Latest News'
        verbose_name_plural = 'Latest News'


class Gifts(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='gifts/')
    order = models.PositiveIntegerField(default=0)  # For manual ordering of gifts

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']



    
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


