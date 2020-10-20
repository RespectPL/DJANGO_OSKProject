from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='loginUser'),
    path('register/', views.registerUser, name='registerUser'),

    path('join_course/', views.joinCourse, name="joinCourse"),
    path('check_course/', views.checkCourse, name="checkCourse"),
    path('complete_your_data/', views.completeDataParticipant, name="completeDataParticipant"),
    path('pay_course/', views.payCourse, name="payCourse"),
    path('check_lectures/', views.checkLectures, name="checkLectures"),
    path('check_driving_lessons/', views.checkDrivingLessons, name="checkDrivingLessons"),
    path('request_change_date_driving_lessons/', views.requestForChangeDateDrivingLesson, name="requestChangeDateDrivingLessons"),
    path('check_internal_exam', views.checkInternalExam, name="checkInternalExam"),

    path('check_participant_course/', views.checkParticipantCourse, name='checkParticipantCourse'),
    path('determine_lecture/', views.determineLecture, name='determineLecture'),
    path('determine_driving_lesson/', views.determineDrivingLesson, name='determineDrivingLesson'),
    path('check_request_change_date_driving_lessons/', views.checkRequestForChangeDateDrivingLesson, name='checkRequestChangeDateDrivingLesson'),
    path('change_date_driving_lesson/', views.changeDateDrivingLesson, name='changeDateDrivingLesson'),
    path('check_lectures_self/', views.checkLecturesSelf, name='checkLecturesSelf'),
    path('check_driving_lessons_self/', views.checkDrivingLessonsSelf, name='checkDrivingLessonSelf'),
    path('complete_course', views.completeCourse, name='completeCourse'),
    path('determine_internal_exam', views.determineInternalExam, name='determineInternalExam'),
]
