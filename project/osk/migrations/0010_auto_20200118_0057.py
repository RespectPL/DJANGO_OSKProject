# Generated by Django 3.0 on 2020-01-17 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osk', '0009_auto_20200117_2324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='termin',
        ),
        migrations.AddField(
            model_name='lecture',
            name='iloscGodzin',
            field=models.CharField(default=str, max_length=2),
            preserve_default=False,
        ),
    ]
