from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atast_web', '0006_ifestvideo_delete_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='ifestImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ifest_bg/')),
            ],
        ),
        migrations.DeleteModel(
            name='ifestVideo',
        ),
    ]
