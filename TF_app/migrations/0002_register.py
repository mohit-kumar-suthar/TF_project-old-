# Generated by Django 3.0.6 on 2020-09-21 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TF_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=12)),
                ('re_password', models.CharField(max_length=12)),
            ],
        ),
    ]
