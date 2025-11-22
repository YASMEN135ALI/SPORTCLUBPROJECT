from django.db import models

from django.contrib.auth.models import User

class Exercise(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image=models.ImageField(upload_to='photo/%y/%m/%d') 
    def __str__(self):
        return f"{self.title} - ${self.price}"


class UserExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ارتباط بالمستخدم
    exercises = models.ManyToManyField(Exercise)  # علاقة متعددة بين المستخدم والتمارين المختارة
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # تخزين المجموع الكلي

    def calculate_total_price(self):
        """ تحديث السعر الإجمالي تلقائيًا عند اختيار التمارين """
        self.total_price = sum(exercise.price for exercise in self.exercises.all())
        self.save()

    def __str__(self):
        return f"{self.user.username} - مجموع السعر: ${self.total_price}"



from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'نقدًا'),
        ('bank', 'تحويل بنكي'),
        ('paypal', 'باي بال'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "مستخدم غير معروف"
        return f"{username} - {self.amount} ريال ({self.get_method_display()})"






# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    SUBSCRIPTION_CHOICES = [
        ('daily', 'يومي'),
        ('monthly', 'شهري'),
        ('yearly', 'سنوي')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    mobile_phone = models.CharField(max_length=15)
    subscription = models.CharField(max_length=10, choices=SUBSCRIPTION_CHOICES)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')
    has_visited = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

from django.db import models
from django.db import models
from django.contrib.auth.models import User

class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المستخدم", null=True,
    blank=True)
    name = models.CharField(max_length=100, verbose_name="الاسم الكامل")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    subject = models.CharField(max_length=200, verbose_name="الموضوع")
    message = models.TextField(verbose_name="نص الرسالة")
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    if self.user and self.subject:
        return f"{self.user.username} - {self.subject}"
    elif self.name and self.subject:
        return f"{self.name} - {self.subject}"
    elif self.subject:
        return f"رسالة بدون اسم - {self.subject}"
    else:
        return "رسالة غير معرّفة"










































class Sport(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(upload_to='sports/', null=True, blank=True)

    def __str__(self):
        return self.name




from django.db import models

class CoursePricing(models.Model):
    sport = models.ForeignKey('Sport', on_delete=models.CASCADE, verbose_name="الرياضة")
    
    base_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="السعر الأساسي")
    group_training_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="سعر التدريب الجماعي")
    private_training_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="سعر التدريب الفردي المخصص")
    single_session_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="سعر الجلسة الواحدة")

    def __str__(self):
        return f"أسعار كورس {self.sport.name}"



class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.ForeignKey(Sport, on_delete=models.CASCADE)
    experience = models.CharField(max_length=50)
    bio = models.TextField()
    image = models.ImageField(upload_to='sports/', null=True, blank=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.value for r in ratings) / ratings.count(), 1)
        return 0

    def __str__(self):
        return self.name









from django.db import models

class Rating(models.Model):
    trainer = models.ForeignKey('Trainer', related_name='ratings', on_delete=models.CASCADE)
    value = models.IntegerField(choices=[(i, f"{i} نجوم") for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # عرض الأحدث أولًا

    def __str__(self):
        return f"{self.trainer.name} - {self.value} نجوم"

















from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User


class TrainingPlan(models.Model):
    GOALS = [
        ('weight_loss', 'خسارة الوزن'),
        ('muscle_gain', 'بناء العضلات'),
        ('fitness', 'تحسين اللياقة'),
        ('relaxation', 'الاسترخاء والتوازن'),
        ('competition', 'تحضير لمسابقة'),
    ]

    TIMES = [
        ('morning', 'الصباح'),
        ('afternoon', 'الظهيرة'),
        ('evening', 'المساء'),
    ]

    DURATIONS = [
        ('session', 'جلسة واحدة'),
        ('week', 'أسبوع'),
        ('month', 'شهر'),
        ('3_months', '3 أشهر'),
        ('custom', 'مدة مخصصة'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=50, choices=GOALS)
    activity = models.CharField(max_length=100)  # اسم الرياضة
    training_type = models.CharField(max_length=20)  # solo or group
    preferred_time = models.CharField(max_length=20, choices=TIMES)
    duration = models.CharField(max_length=20, choices=DURATIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"خطة {self.user.username} - {self.get_goal_display()}"



class SportPricing(models.Model):
    SPORT_TYPES = [
        ('football', 'كرة القدم'),
        ('yoga', 'يوغا'),
        ('boxing', 'ملاكمة'),
        # أضف المزيد حسب الحاجة
    ]

    SESSION_TYPES = [
        ('solo', 'فردي'),
        ('group', 'جماعي'),
        ('custom', 'مخصص'),
    ]

    sport_name = models.CharField(max_length=50, choices=SPORT_TYPES)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.get_sport_name_display()} - {self.get_session_type_display()}"


# models.py
from django.db import models

# قصص النجاح
class SuccessStory(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    quote = models.TextField()
    image = models.ImageField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – {self.age} سنة"

# الأبطال الأسبوعيين
class WeeklyChampion(models.Model):
    name = models.CharField(max_length=100)
    achievement = models.TextField()
    week = models.DateField()
    icon = models.CharField(max_length=10, default="🏅")

    def __str__(self):
        return f"{self.name} – {self.week}"


# نصائح المدربين
class TrainerTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title










from django.db import models

class ClubPulse(models.Model):
    CATEGORY_CHOICES = [
        ('announcement', 'إعلان'),
        ('competition', 'مسابقة'),
        ('offer', 'عرض'),
    ]

    title = models.CharField(max_length=200, verbose_name="العنوان")
    content = models.TextField(verbose_name="المحتوى")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="النوع")
    publish_date = models.DateField(verbose_name="تاريخ النشر")
    expire_date = models.DateField(verbose_name="تاريخ الانتهاء")

def __str__(self):
        return f"{self.get_category_display()} - {self.title}"









class NewPayment(models.Model):
    METHOD_CHOICES = [
        ('cash', 'نقدًا'),
        ('bank', 'تحويل بنكي'),
        ('paypal', 'باي بال'),
    ]

    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "مستخدم غير معروف"
        return f"{username} - {self.amount} ريال ({self.get_method_display()})"

    class Meta:
        db_table = 'new_payment'
