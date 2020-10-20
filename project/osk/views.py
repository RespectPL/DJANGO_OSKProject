from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm, CheckCourseForm, CompleteDataParticipantForm, DetermineLectureForm,\
    DetermineDrivingLessonForm, RequestForChangeDateDrivingLessonForm, ChangeDateDrivingLessonForm, CompleteCourseForm,\
    DetermineInternalExamForm
from .models import CourseData, Participant, Course, Lecture, DrivingLesson, RequestForChangeDateDrivingLesson,\
    InternalExam
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import re
import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')

def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["login"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Zostałeś zalogowany!")
            else:
                messages.warning(request, "Błąd logowania! Popraw dane i spróbuj ponownie.")
    if request.user.is_authenticated:
        return redirect('/osk/')
    else:
        form = LoginForm()
        return render(request, 'login.html', { 'form' : form })

def registerUser(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST["login"]
            first_name = request.POST["imie"]
            last_name = request.POST["nazwisko"]
            email = request.POST["email"]
            password = request.POST["password"]
            user,created = User.objects.get_or_create(username=username, email=email, first_name=first_name, last_name=last_name)
            if created:
                user.set_password(password)
                user.save()
                messages.success(request, "Zarejestrowano pomyślnie! Możesz się już zalogować.")
                return redirect('/osk/')
            else:
                messages.warning(request, "Użytkownik istnieje w bazie!")
    if not request.user.is_authenticated:
        form = RegisterForm()
        return render(request, 'register.html', { 'form' : form })
    else:
        redirect('/osk/')

def joinCourse(request):
    if request.method == 'POST':
        form = CheckCourseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kategoria = data.get('kategoria')
            user = request.user.username
            checkCourseUser = CourseData.objects.filter(user=user, kurs=kategoria)
            if len(checkCourseUser) == 0:
                CourseData.objects.create(user=user, kurs=kategoria, paid=False, completed=False)
                messages.success(request, "Pomyślnie zapisano na kurs!")
            else:
                messages.warning(request, "Jesteś już zapisany na ten kurs!")
        else:
            messages.warning(request, "Błąd formularza.")
    else:
        form = CheckCourseForm()
    return render(request, 'join_course.html', { 'form' : form })

def checkCourse(request):
    courses = CourseData.objects.filter(user=request.user.username)
    check = False
    for c in courses:
        if not c.paid:
            messages.warning(request, "Masz nieopłacone kursy!")
            check = True
            break
    return render(request, 'check_course.html', { 'courses' : courses, 'check' : check })

def completeDataParticipant(request):
    datas = Participant.objects.filter(user=request.user.username)
    if request.method == 'POST':
        form = CompleteDataParticipantForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pesel = data.get('pesel')
            telefon = data.get('telefon')
            pkk = data.get('pkk')
            user = request.user.username
            imie = request.user.first_name
            nazwisko = request.user.last_name
            if len(datas) == 0:
                if re.match('[0-9]{11}$', pesel) and re.match('[0-9]{11}$', telefon) and re.match('[0-9]{20}$', pkk):
                    Participant.objects.create(imie=imie, nazwisko=nazwisko, telefon=telefon, pesel=pesel, user=user, pkk=pkk)
                    messages.success(request, "Twoje dane zostały zapisane!")
                else:
                    messages.warning("Niepoprawne dane! Popraw je i spróbuj ponownie")
            else:
                if pesel != "":
                    if re.match('[0-9]{11}$', pesel):
                        Participant.objects.filter(user=user).update(pesel=pesel)
                        messages.success(request, "PESEL został zaktualizowany!")
                    else:
                        messages.warning(request, "Niepoprawny PESEL!")
                if telefon != "":
                    if re.match('[0-9]{20}$', telefon):
                        Participant.objects.filter(user=user).update(telefon=telefon)
                        messages.success(request, "Numer telefonu został zaktualizowany!")
                    else:
                        messages.warning(request, "Niepoprawny numer telefonu!")
                if pkk != "":
                    if re.match('[0-9]{20}$', pkk):
                        Participant.objects.filter(user=user).update(pkk=pkk)
                        messages.success(request, "Numer PKK został zaktualizowany!")
                    else:
                        messages.warning(request, "Niepoprawny numer PKK!")
        else:
            messages.warning(request, "Błąd formularza.")
    else:
        if len(datas) > 0:
            messages.warning(request, "Twoje dane są już uzupełnione! Jeśli chcesz zmienić dane wypełnij poniższy formularz.")
        form = CompleteDataParticipantForm()
    return render(request, 'complete_data_participant.html', { 'form' : form })

def payCourse(request):
    if request.method == 'POST':
        data = request.POST["kurs"]
        spl = data.split("/")
        kurs = Course.objects.filter(oznaczenie=spl[0])
        CourseData.objects.filter(user=request.user.username, kurs=kurs[0]).update(paid=True)
        messages.success(request, "Zapłaciłeś za kurs!")
        return redirect('/osk/')
    else:
        courses = CourseData.objects.filter(user=request.user.username, paid=False)
        return render(request, 'pay_course.html', { 'courses' : courses })

def checkParticipantCourse(request):
    courses = CourseData.objects.all()
    datas = []
    for c in courses:
        username = c.user
        u = User.objects.get(username=username)
        datas.append((u.first_name, u.last_name, u.username, c.kurs, c.paid, c.completed))
    return render(request, 'check_participant_courses.html', {'datas' : datas })

def determineLecture(request):
    if request.method == 'POST':
        form = DetermineLectureForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kursant = data.get('kursant')
            user = kursant.user
            temat = data.get('temat')
            date = data.get('data')
            godzina = data.get('godzina')
            ilosc = data.get('iloscGodzin')
            instruktor = request.user.first_name + " " + request.user.last_name
            Lecture.objects.create(instruktorUser=request.user.username, instruktor=instruktor, kursant=user, temat=temat, data=date, godzina=godzina, iloscGodzin=ilosc)
            messages.success(request, "Ustalono wykład pomyślnie!")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = DetermineLectureForm()
    return render(request, 'determine_lecture.html', { 'form' : form })

def checkLectures(request):
    lectures = Lecture.objects.filter(kursant=request.user.username)
    nadchodzace = False
    licznik = 0
    for l in lectures:
        licznik += int(l.iloscGodzin)
        if l.data >= datetime.date.today():
            nadchodzace = True
            l.n = True
        elif l.data == datetime.date.today():
            if l.godzina >= datetime.datetime.now().time():
                l.n = True
                nadchodzace = True
            else:
                l.n = False
        else:
            l.n = False
    if nadchodzace:
        messages.warning(request, "Masz wykłady ustalone w najbliższym czasie! Sprawdź terminy.")
    messages.success(request, "Masz odbyte (lub ustalone) " + str(licznik) + "/10 h wykładów!")
    return render(request, 'check_lecture.html', {'lectures' : lectures })

def determineDrivingLesson(request):
    if request.method == 'POST':
        form = DetermineDrivingLessonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kursant = data.get('kursant')
            user = kursant.user
            pojazd = data.get('pojazd')
            kurs = data.get('kurs')
            date = data.get('data')
            godzina = data.get('godzina')
            ilosc = data.get('iloscGodzin')
            instruktor = request.user.first_name + " " + request.user.last_name
            DrivingLesson.objects.create(instruktorUser=request.user.username, instruktor=instruktor, kursant=user, vehicle=pojazd, kurs=kurs, data=date, godzina=godzina, iloscGodzin=ilosc)
            messages.success(request, "Ustalono jazdę pomyślnie!")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = DetermineDrivingLessonForm()
    return render(request, 'determine_driving_lesson.html', { 'form' : form })

def checkDrivingLessons(request):
    dls = DrivingLesson.objects.filter(kursant=request.user.username).order_by(('-data'))
    nadchodzace = False
    for dl in dls:
        if dl.data > datetime.date.today():
            dl.n = True
            nadchodzace = True
        elif dl.data == datetime.date.today():
            if dl.godzina >= datetime.datetime.now().time():
                dl.n = True
                nadchodzace = True
            else:
                dl.n = False
        else:
            dl.n = False
    courses = Course.objects.all()
    for c in courses:
        licznik = 0
        dlss = DrivingLesson.objects.filter(kursant=request.user.username, kurs=c)
        for d in dlss:
            licznik += int(d.iloscGodzin)
        if (licznik > 0):
                messages.success(request, "Masz wyjeżdżone (lub ustalone) " + str(licznik) + "/30 h jazd (KURS: " + str(d.kurs) + ")!")
    if nadchodzace:
        messages.warning(request, "Masz jazdy ustalone w najbliższym czasie! Sprawdź terminy.")
    return render(request, 'check_driving_lesson.html', {'dls' : dls })

def requestForChangeDateDrivingLesson(request):
    if request.method == 'POST':
        form = RequestForChangeDateDrivingLessonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instruktor = data.get('instruktor')
            instr = instruktor.user
            prosba = data.get('prosba')
            date = datetime.datetime.now()
            user = request.user.username
            RequestForChangeDateDrivingLesson.objects.create(instruktor=instr, kursant=user, data=date, prosba=prosba)
            messages.success(request, "Wysłano prośbę do instruktora! Sprawdzaj na bieżąco, czy termin został zmieniony.")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = RequestForChangeDateDrivingLessonForm()
    return render(request, 'request_change_driving_lesson.html', {'form' : form })

def checkRequestForChangeDateDrivingLesson(request):
    req = RequestForChangeDateDrivingLesson.objects.filter(instruktor=request.user.username).order_by('data')
    return render(request, 'check_request_change_date.html', {'req' : req })

def changeDateDrivingLesson(request):
    if request.method == 'POST':
        form = ChangeDateDrivingLessonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            dl = data.get('jazda')
            date = data.get('data')
            godzina = data.get('godzina')
            iloscGodzin = data.get('iloscGodzin')
            krsnt = DrivingLesson.objects.filter(kursant=dl.kursant, data=dl.data, godzina=dl.godzina)
            if len(krsnt) > 0:
                DrivingLesson.objects.filter(kursant=dl.kursant, data=dl.data, godzina=dl.godzina).update(data=date, godzina=godzina, iloscGodzin=iloscGodzin)
                messages.success(request, "Zmieniono termin jazdy!")
            else:
                messages.warning(request, "Nie ma takiej jazdy!")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = ChangeDateDrivingLessonForm()
    return render(request, 'change_driving_lesson.html', { 'form' : form })

def checkDrivingLessonsSelf(request):
    dls = DrivingLesson.objects.filter(instruktorUser=request.user.username).order_by('kursant', '-data')
    for dl in dls:
        user = User.objects.filter(username=dl.kursant)[0]
        dl.us = user.first_name + " " + user.last_name
        if dl.data >= datetime.date.today():
            dl.n = True
        elif dl.data == datetime.date.today():
            if dl.godzina >= datetime.datetime.now().time():
                dl.n = True
            else:
                dl.n = False
        else:
            dl.n = False
    return render(request, 'check_driving_lesson_self.html', {'dls' : dls })

def checkLecturesSelf(request):
    lectures = Lecture.objects.filter(instruktorUser=request.user.username).order_by('kursant', '-data')
    for l in lectures:
        user = User.objects.filter(username=l.kursant)[0]
        l.us =  user.first_name + " " + user.last_name
        if l.data >= datetime.date.today():
            l.n = True
        elif l.data == datetime.date.today():
            if l.godzina >= datetime.datetime.now().time():
                l.n = True
            else:
                l.n = False
        else:
            l.n = False
    return render(request, 'check_lecture_self.html', {'lectures' : lectures })

def completeCourse(request):
    if request.method == 'POST':
        form = CompleteCourseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kurs = data.get('kurs')
            kursant = kurs.user
            course = kurs.kurs
            CourseData.objects.filter(user=kursant, kurs=course).update(completed=True)
            messages.success(request, "Pomyślnie zakończono kurs!")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = CompleteCourseForm()
    return render(request, 'complete_course.html', { 'form' : form })

def determineInternalExam(request):
    if request.method == 'POST':
        form = DetermineInternalExamForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            kursant = data.get('kursant')
            krsnt = kursant.user
            kurs = data.get('kurs')
            date = data.get('data')
            godzina = data.get('godzina')
            instruktor = request.user.username
            InternalExam.objects.create(instruktor=instruktor, kursant=krsnt, kurs=kurs, data=date, godzina=godzina)
            messages.success(request, "Pomyślnie ustalono egzamin wewnętrzny!")
        else:
            messages.warning(request, "Błąd formularza")
    else:
        form = DetermineInternalExamForm()
    return render(request, 'determine_internal_exam.html', { 'form' : form })

def checkInternalExam(request):
    ies = InternalExam.objects.filter(kursant=request.user.username)
    nadchodzace = False
    for ie in ies:
        user = User.objects.filter(username=ie.instruktor)[0]
        ie.us =  user.first_name + " " + user.last_name
        if ie.data >= datetime.date.today():
            ie.n = True
            nadchodzace = True
        elif ie.data == datetime.date.today():
            if ie.godzina >= datetime.datetime.now().time():
                ie.n = True
                nadchodzace = True
            else:
                ie.n = False
        else:
            ie.n = False
        if nadchodzace:
            messages.warning(request, "Masz ustalone i nadchodzące egzaminy wewnętrzne!")
    return render(request, 'check_internal_exam.html', { 'ies' : ies })