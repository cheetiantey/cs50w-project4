# Generated by Django 3.1.7 on 2021-03-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20210312_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, related_name='liked', to='network.Post'),
        ),
    ]
