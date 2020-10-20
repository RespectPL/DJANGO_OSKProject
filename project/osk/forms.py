from django import forms
from .models import Course, Participant, Vehicle, Instructor, DrivingLesson, CourseData

class LoginForm(forms.Form):
    loginClass = forms.TextInput(attrs={'class' : 'form-control'})
    passwordClass = forms.PasswordInput(attrs={'class' : 'form-control'})
    login = forms.CharField(widget=loginClass, label="Login", max_length=50, required=True)
    password = forms.CharField(widget=passwordClass, label="Hasło", max_length=50, required=True)

class RegisterForm(forms.Form):
    txtClass = forms.TextInput(attrs={'class' : 'form-control'})
    passwordClass = forms.PasswordInput(attrs={'class' : 'form-control'})
    login = forms.CharField(widget=txtClass, label="Login", max_length=50, required=True)
    imie = forms.CharField(widget=txtClass, label="Imię", max_length=30, required=True)
    nazwisko = forms.CharField(widget=txtClass, label="Nazwisko", max_length=30, required=True)
    email = forms.CharField(widget=txtClass, label="E-mail", max_length=250, required=True)
    password = forms.CharField(widget=passwordClass, label="Hasło", max_length=50, required=True)

class CheckCourseForm(forms.Form):
    kategoria = forms.ModelChoiceField(label="Kategoria", queryset=Course.objects.order_by('oznaczenie'), required=True)

class CompleteDataParticipantForm(forms.Form):
    txtClass = forms.TextInput(attrs={'class': 'form-control'})
    pesel = forms.CharField(widget=txtClass, label="PESEL", max_length=11, required=False)
    telefon = forms.CharField(widget=txtClass, label="Telefon", max_length=11, required=False)
    pkk = forms.CharField(widget=txtClass, label="Numer PKK", max_length=50, required=False)

class DetermineLectureForm(forms.Form):
    kursant = forms.ModelChoiceField(queryset=Participant.objects.order_by('nazwisko'), required=True)
    temat = forms.CharField(label="Temat", max_length=300, required=True)
    data = forms.DateField(required=True)
    godzina = forms.TimeField(required=True)
    iloscGodzin = forms.CharField(label="Ilość godzin", max_length=2, required=True)

class DetermineDrivingLessonForm(forms.Form):
    kursant = forms.ModelChoiceField(queryset=Participant.objects.order_by('nazwisko'), required=True)
    pojazd = forms.ModelChoiceField(queryset=Vehicle.objects.order_by('nrRejestracyjny'), required=True)
    kurs = forms.ModelChoiceField(queryset=Course.objects.order_by('oznaczenie'), required=True)
    data = forms.DateField(required=True)
    godzina = forms.TimeField(required=True)
    iloscGodzin = forms.CharField(max_length=2, required=True)

class RequestForChangeDateDrivingLessonForm(forms.Form):
    instruktor = forms.ModelChoiceField(queryset=Instructor.objects.order_by('nazwisko'), required=True)
    prosba = forms.CharField()

class ChangeDateDrivingLessonForm(forms.Form):
    jazda = forms.ModelChoiceField(queryset=DrivingLesson.objects.order_by('kursant'), required=True)
    data = forms.DateField(required=True)
    godzina = forms.TimeField(required=True)
    iloscGodzin = forms.CharField(max_length=2, required=True)

class CompleteCourseForm(forms.Form):
    kurs = forms.ModelChoiceField(queryset=CourseData.objects.filter(completed=False).order_by('user'), required=True)

class DetermineInternalExamForm(forms.Form):
    kursant = forms.ModelChoiceField(queryset=Participant.objects.order_by('nazwisko'), required=True)
    kurs = forms.ModelChoiceField(queryset=Course.objects.order_by('oznaczenie'), required=True)
    data = forms.DateField()
    godzina = forms.TimeField()
