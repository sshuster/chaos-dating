# Generated by Django 3.0.2 on 2020-02-29 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chaos_dating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='wishes',
            field=models.ManyToManyField(blank=True, to='chaos_dating.Wish'),
        ),
    ]
