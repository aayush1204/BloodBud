# Generated by Django 3.1.6 on 2021-03-13 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0007_location_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bloodgroup',
            field=models.CharField(default='O+', max_length=2),
        ),
    ]