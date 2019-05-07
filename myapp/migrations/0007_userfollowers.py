# Generated by Django 2.1.5 on 2019-05-07 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_user_isactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowers',
            fields=[
                ('relation_id', models.AutoField(primary_key=True, serialize=False)),
                ('followee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followee_profile', to='myapp.User')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_profile', to='myapp.User')),
            ],
        ),
    ]
