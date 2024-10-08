# Generated by Django 4.1.7 on 2023-09-20 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_following_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=255)),
                ('commented', models.DateTimeField(auto_now_add=True)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL)),
                ('main_post', models.ForeignKey(default='Post deleted.', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='comments', to='network.post')),
            ],
            options={
                'ordering': ['-commented'],
            },
        ),
    ]
