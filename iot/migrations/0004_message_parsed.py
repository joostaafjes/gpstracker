# Generated by Django 3.2.7 on 2021-10-02 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0003_alter_message_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='parsed',
            field=models.BooleanField(default=False),
        ),
    ]
