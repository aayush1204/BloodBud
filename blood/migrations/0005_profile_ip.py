# Generated by Django 3.1.6 on 2021-03-13 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ip',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
