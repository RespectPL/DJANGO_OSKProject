# Generated by Django 3.0.2 on 2020-01-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osk', '0005_auto_20200115_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedata',
            name='completed',
            field=models.BooleanField(default=bool),
            preserve_default=False,
        ),
    ]
