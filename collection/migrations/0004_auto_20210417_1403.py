# Generated by Django 2.2.19 on 2021-04-17 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_movie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='collection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
    ]
