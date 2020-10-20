from django.contrib import admin
from .models import Course, Participant, CourseData, Lecture, Vehicle, DrivingLesson, Instructor,\
    RequestForChangeDateDrivingLesson, InternalExam

# Register your models here.
class CourseDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'kurs', 'paid', 'completed')
class CourseAdmin(admin.ModelAdmin):
    list_display = ('oznaczenie', 'kategoria')
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'imie', 'nazwisko', 'pesel', 'telefon', 'pkk')
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('nrRejestracyjny', 'typ', 'nazwa')
class InstructorAdmin(admin.ModelAdmin):
    list_display =  ('nazwisko', 'imie', 'user')
class RequestForChangeDateDrivingLessonAdmin(admin.ModelAdmin):
    list_display = ('kursant', 'instruktor', 'data', 'prosba')
admin.site.register(Course, CourseAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(CourseData, CourseDataAdmin)
admin.site.register(Lecture)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(DrivingLesson)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(RequestForChangeDateDrivingLesson, RequestForChangeDateDrivingLessonAdmin)
admin.site.register(InternalExam)