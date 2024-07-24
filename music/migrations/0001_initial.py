# Generated by Django 5.0.3 on 2024-07-23 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('file_upload', models.FileField(upload_to='music/')),
            ],
        ),
    ]
