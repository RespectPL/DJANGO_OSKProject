# Generated by Django 3.0.2 on 2020-01-15 20:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('oznaczenie', models.CharField(max_length=5)),
                ('kategoria', models.CharField(max_length=150)),
            ],
        ),
    ]
