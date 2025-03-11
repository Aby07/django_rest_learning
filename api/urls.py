
from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('viewsetEmployeeDetail', views.ViewSetEmployeeView, basename='employee')
router.register('ModelViewsetEmployeeDetail', views.ModelViewSetEmployeeView, basename='modelviewsetemployee')

urlpatterns = [
    path('studentsview/', views.studentsView, name='studentView'),
    path('studentDetailView/<int:pk>/', views.studentDetailView, name='studentDetailView'),

    path('employeesView/', views.Employees.as_view()), #CBV
    path('employeeDetail/<int:pk>/', views.EmployeeDetail.as_view()), #CBV for get single employee details

    path('employeesMixinView/', views.MixinEmployees.as_view()), # mixin
    path('employeeMixinDetail/<int:pk>/', views.MixinEmployeeDetail.as_view()), #CBV for get single employee details

    path('GenericEmployeeView/', views.GenericEmployee.as_view()), # generics
    path('genericEmployeeDetail/<int:pk>/', views.GenericEmployeeDetail.as_view()), #CBV for get single employee details

    path('blogs/', views.BlogViews.as_view()),
    path('comments/', views.CommentsViews.as_view()),

    path('blogs/<int:pk>/', views.BlogDetailViews.as_view()),
    path('comments/<int:pk>/', views.CommentsDetailViews.as_view())
]

urlpatterns += router.urls

 