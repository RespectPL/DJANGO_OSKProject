# Generated by Django 3.0 on 2020-01-21 23:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('osk', '0016_instructor_requestforchangedatedrivinglesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalExam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('instruktor', models.CharField(max_length=200)),
                ('kursant', models.CharField(max_length=200)),
                ('data', models.DateField()),
                ('godzina', models.TimeField()),
                ('kurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osk.Course')),
            ],
        ),
    ]