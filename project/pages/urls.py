from django.urls import path
from . import views
from .views import make_payment, payment_success , contact_us,create_plan
from .views import custom_logout_view
from .views import create_plan_and_process_payment


urlpatterns = [
    path('', views.index, name='index'),
   path('about/', views.about_page, name='about'),


   path('login/', views.login_user, name='custom_login'),

    path('success/', views.success, name='success_page'),
    path('exersies/', views.exercise_list, name='exercise_list'),
    path('make-payment/<int:plan_id>/', views.make_payment, name='make_payment'),

    path('success/<int:payment_id>/', payment_success, name='payment_success'),
    path('contact/', views.contact_us, name='contact'),
    path('trainers/', views.sports_and_trainers, name='sports_and_trainers'),  # ✅ تعديل هنا
    path('rate/<int:trainer_id>/', views.rate_trainer, name='rate_trainer'),
     path('create-plan/', create_plan_and_process_payment, name='create_plan'),
    path('my-plan/', views.my_plan, name='my_plan'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
   path('register/', views.register_user, name='register'),

  

 
    


    path('logout/', custom_logout_view, name='logout'),

]













 


