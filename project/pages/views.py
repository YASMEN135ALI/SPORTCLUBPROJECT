import json
from django.utils.safestring import mark_safe

from django.shortcuts import render, redirect
from .models import Payment,Exercise, UserExercise
from django.contrib.auth.hashers import make_password
from django.db.models import Sum

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import Profile
from django.contrib import messages  # تأكد من استيرادها

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import TrainingPlan, Rating, Profile


from .models import TrainingPlan
from django.shortcuts import render 
from django.contrib.auth.decorators import login_required


from .models import TrainingPlan, Payment
from .tests import calculate_plan_price, generate_transaction_id, process_payment

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TrainingPlan

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TrainingPlan

 # +صفحه النجاح الصفحه الرئيسيه

def index(request):
  x={'name':'ahmed','age':4444}
  return render(request,'pages/index.html',x)

def success(request):
      return render(request,'pages/success_page.html')





# accounts/انشاء حساب

def register_user(request):
    if request.method == 'POST':
        # استلام البيانات
        username = request.POST['username']
        email = request.POST['email_address']
        age = request.POST['age']
        password = request.POST['password']
        mobile = request.POST['mobile_phone']
        subscription = request.POST['subscription']

        # التحقق من قوة كلمة المرور
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'pages/register.html', {'error': e.messages})

        # إنشاء المستخدم
        user = User.objects.create_user(username=username, email=email, password=password)

        # إنشاء البروفايل
        Profile.objects.create(
            user=user,
            age=age,
            mobile_phone=mobile,
            subscription=subscription
        )

        login(request, user)

        # ✅ إضافة الرسالة الترحيبية
        messages.success(request, "🎉 يسرنا انضمامك! يمكنك الآن زياره مقر النادي وبدء رحلتك داخل النادي.")

        return redirect('profile')

    return render(request, 'pages/register.html')

#صفحه الحساب الشخصيز  
@login_required
def profile(request):
       profile = request.user.profile
       return render(request, 'pages/profile.html', {'profile': profile})

#صفحه تسجيل الدخول 
from django.contrib.auth import authenticate, login
def login_user(request):
       if request.method == 'POST':
           username = request.POST['username']
           password = request.POST['password']
           user = authenticate(request, username=username, password=password)
           if user is not None:
               login(request, user)
               return redirect('profile')
           else:
               return render(request, 'pages/login.html', {'error': 'بيانات الدخول غير صحيحة'})
       return render(request, 'pages/login.html')
# صفحه تعديل البيانات الشخصيه للمستخدم

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileForm
@login_required
def edit_profile(request):
       profile = request.user.profile
       if request.method == 'POST':
           form = ProfileForm(request.POST, request.FILES, instance=profile)
           if form.is_valid():
               form.save()
               return redirect('profile')
       else:
           form = ProfileForm(instance=profile)
       return render(request, 'pages/edit_profile.html', {'form': form})

#صفحه انشاء الدددفففعععع
from django.shortcuts import render, redirect
from .models import Payment
from django.contrib.auth.decorators import login_required
import uuid
from .models import Payment, TrainingPlan
from .tests import generate_transaction_id  # أو من utils حسب اسم الملف
from .models import NewPayment  # أو whatever اسم النموذج الجديد


@login_required

def make_payment(request, plan_id):
    try:
        plan = TrainingPlan.objects.get(id=plan_id, user=request.user)
    except TrainingPlan.DoesNotExist:
        return render(request, 'pages/make_payment.html', {'error': 'الخطة غير موجودة أو غير مسموح بها.'})

    amount = calculate_plan_price(plan)

    if request.method == 'POST':
        method = request.POST.get('method')

        if method not in dict(Payment.METHOD_CHOICES):
            return render(request, 'pages/make_payment.html', {
                'error': 'طريقة الدفع غير صالحة.',
                'plan': plan,
                'amount': amount
            })

        payment = Payment.objects.create(
            user=request.user,
            method=method,
            amount=amount,
            status='completed',
            transaction_id=generate_transaction_id()
        )

        plan.payment = payment
        plan.is_paid = True
        plan.is_active = True
        plan.save()

        return redirect('payment_success', payment_id=payment.id)

    return render(request, 'pages/make_payment.html', {
        'plan': plan,
        'amount': amount
    })

#صفحه التوااااااااااااااااااصل
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال رسالتك بنجاح! سنقوم بالرد عليك قريبًا.')
            return redirect('contact')  # تأكد أن اسم الرابط هو نفسه في urls.py
    else:
        form = ContactForm()
    return render(request, 'pages/contact_us.html', {'form': form})







#سلسله التمارين للحذف
def exercise_list(request):
    exercises = UserExercise.objects.all()
    return render(request, 'exercise_list.html', {'exercises': exercises})


def toggle_exercise_selection(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # جلب أو إنشاء سجل UserExercise للمستخدم الحالي
    user_exercise, created = UserExercise.objects.get_or_create(user=request.user)

    if exercise in user_exercise.exercises.all():
        # إذا التمرين موجود، نحذفه
        user_exercise.exercises.remove(exercise)
        status = 'deselected'
    else:
        # إذا التمرين غير موجود، نضيفه
        user_exercise.exercises.add(exercise)
        status = 'selected'

    # تحديث المجموع الكلي
    user_exercise.calculate_total_price()

    return JsonResponse({
        'status': status,
        'exercise': exercise.title,
        'total_price': float(user_exercise.total_price)
    })






#نجاح الدفع  

from django.shortcuts import render, get_object_or_404
from .models import Payment, ContactMessage


def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payment_success.html', {'payment': payment})
























#صفحه المدربين والرياضات

from .models import Sport, CoursePricing

def sports_and_trainers(request):
    sports = Sport.objects.all()
    course_pricing = CoursePricing.objects.select_related('sport').order_by('sport__name')

    context = {
        'sports': sports,
        'course_pricing': course_pricing
    }

    return render(request, 'pages/sports_and_trainers.html', context)


# trainers/المدربيت
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Trainer, Rating

@require_POST
def rate_trainer(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    
    # استلام البيانات من النموذج
    value = int(request.POST.get('value', 0))
    comment = request.POST.get('comment', '').strip()

    # التحقق من صحة التقييم
    if value in range(1, 6):
        Rating.objects.create(
            trainer=trainer,
            value=value,
            comment=comment
        )

    # إعادة التوجيه إلى صفحة المدربين
    return redirect('sports_and_trainers')










#خاص بانشاء الخطه


@login_required
def create_plan(request):
    if request.method == 'POST':
        goal = request.POST.get('goal')
        activity = request.POST.get('activity')
        training_type = request.POST.get('training_type')
        preferred_time = request.POST.get('preferred_time')
        duration = request.POST.get('duration')

        if not all([goal, activity, training_type, preferred_time, duration]):
            return render(request, 'pages/create_plan.html', {'error': 'يرجى تعبئة جميع الحقول'})

        plan = TrainingPlan.objects.create(
            user=request.user,
            goal=goal,
            activity=activity,
            training_type=training_type,
            preferred_time=preferred_time,
            duration=duration
        )

        # التوجيه إلى صفحة الدفع مع plan_id
        return redirect('payment_page', plan_id=plan.id)

    return render(request, 'pages/create_plan.html')












# views.py/صفحه من نحن
from django.shortcuts import render
from .models import SuccessStory, WeeklyChampion, TrainerTip
from datetime import date

from django.utils import timezone

def about_page(request):
    today = timezone.localdate()

    stories = SuccessStory.objects.order_by('-created_at')
    champions = WeeklyChampion.objects.filter(week__lte=today).order_by('-week')
    tips = TrainerTip.objects.order_by('-date')
    club_pulse = ClubPulse.objects.filter(
        publish_date__lte=today,
        expire_date__gte=today
    ).order_by('-publish_date')

    return render(request, 'pages/about.html', {
        'stories': stories,
        'champions': champions,
        'tips': tips,
        'club_pulse': club_pulse
    })

#داله تسجيل الخروج
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('index')  # أو أي صفحة تريد إعادة التوجيه إليها


















# views.py انشاء الخطه مع الدفع


@login_required
def create_plan_and_process_payment(request):
    if request.method == 'POST':
        user = request.user
        plan_data = {
            'goal': request.POST.get('goal'),
            'activity': request.POST.get('activity'),
            'training_type': request.POST.get('training_type'),
            'preferred_time': request.POST.get('preferred_time'),
            'duration': request.POST.get('duration'),
        }

        if not all(plan_data.values()):
            return render(request, 'pages/create_plan.html', {
                'error': 'يرجى تعبئة جميع الحقول'
            })

        plan = TrainingPlan.objects.create(user=user, **plan_data)

        # ✅ إضافة رسالة تأكيد
        messages.success(request, 'و  تم إنشاء الخطة التدريبية بنجاح! يمكنك الآن إتمام الدفع.وزياره مقر النادي باي وقت ترغب')

        # التوجيه إلى صفحة الدفع
        return redirect('make_payment', plan_id=plan.id)

    return render(request, 'pages/create_plan.html')











#عرض الخطه

@login_required
def my_plan(request):
    plan = TrainingPlan.objects.filter(user=request.user).last()
    return render(request, 'my_plan.html', {'plan': plan})



#فقره نبضات النادي

from django.shortcuts import render
from .models import ClubPulse
from django.utils import timezone

def club_pulse_view(request):
    today = timezone.localdate()
    club_pulse = ClubPulse.objects.filter(
        publish_date__lte=today,
        expire_date__gte=today
    ).order_by('-publish_date')

    return render(request, 'pages/about.html', {'club_pulse': club_pulse})
