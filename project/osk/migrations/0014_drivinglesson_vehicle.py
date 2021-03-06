# Generated by Django 3.0 on 2020-01-18 21:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('osk', '0013_lecture_instruktoruser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('typ', models.CharField(max_length=100)),
                ('nazwa', models.CharField(max_length=150)),
                ('nrRejestracyjny', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='DrivingLesson',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=200)),
                ('data', models.DateField()),
                ('godzina', models.TimeField()),
                ('iloscGodzin', models.CharField(max_length=2)),
                ('kurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osk.Course')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osk.Vehicle')),
            ],
        ),
    ]
