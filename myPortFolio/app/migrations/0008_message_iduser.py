# Generated by Django 5.0.3 on 2024-05-02 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='idUser',
            field=models.IntegerField(default=1),
        ),
    ]
