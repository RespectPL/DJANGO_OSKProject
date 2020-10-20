from django.db import models
import uuid

# Create your models here.
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oznaczenie = models.CharField(max_length=5)
    kategoria = models.CharField(max_length=150)

    def __str__(self):
        return self.oznaczenie + "/" + self.kategoria

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=200)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    pesel = models.CharField(max_length=12)
    telefon = models.CharField(max_length=12)
    pkk = models.CharField(max_length=50)

    def __str__(self):
        return self.imie + " " + self.nazwisko + " (" + self.user + ")"

class CourseData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=200)
    kurs = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField()
    completed = models.BooleanField()

    def __str__(self):
        return self.user + " (kurs " + self.kurs.oznaczenie + ")"

class Lecture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instruktorUser = models.CharField(max_length=200)
    instruktor = models.CharField(max_length=200)
    kursant = models.CharField(max_length=200)
    temat = models.CharField(max_length=300)
    data = models.DateField()
    godzina = models.TimeField()
    iloscGodzin = models.CharField(max_length=2)

class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    typ = models.CharField(max_length=100)
    nazwa = models.CharField(max_length=150)
    nrRejestracyjny = models.CharField(max_length=8)

    def __str__(self):
        return self.nrRejestracyjny + "/" + self.nazwa + "/" + self.typ

class DrivingLesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instruktorUser = models.CharField(max_length=200)
    instruktor = models.CharField(max_length=200)
    kursant = models.CharField(max_length=200)
    kurs = models.ForeignKey(Course, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    data = models.DateField()
    godzina = models.TimeField()
    iloscGodzin = models.CharField(max_length=2)

    def __str__(self):
        return self.kursant + " : " + self.kurs.__str__() + " (" + str(self.data) + " - " + str(self.godzina) + ")"

class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=200)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)

    def __str__(self):
        return self.imie + " " + self.nazwisko

class RequestForChangeDateDrivingLesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instruktor = models.CharField(max_length=200)
    kursant = models.CharField(max_length=200)
    data = models.DateTimeField()
    prosba = models.TextField()

class InternalExam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instruktor = models.CharField(max_length=200)
    kursant = models.CharField(max_length=200)
    kurs = models.ForeignKey(Course, on_delete=models.CASCADE)
    data = models.DateField()
    godzina = models.TimeField()