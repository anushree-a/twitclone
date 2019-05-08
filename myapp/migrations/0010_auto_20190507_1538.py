# Generated by Django 2.1.5 on 2019-05-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20190507_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='email', max_length=80),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=280, unique=True),
        ),
    ]