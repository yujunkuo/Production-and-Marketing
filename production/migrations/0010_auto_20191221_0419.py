# Generated by Django 2.2.5 on 2019-12-21 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0009_auto_20191221_0348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='made',
            name='id',
        ),
        migrations.RemoveField(
            model_name='order',
            name='id',
        ),
        migrations.AlterField(
            model_name='made',
            name='mTime',
            field=models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='oTime',
            field=models.DateTimeField(auto_now_add=True, primary_key=True, serialize=False),
        ),
    ]