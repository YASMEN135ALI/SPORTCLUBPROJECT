from django.contrib import admin
from .models import TrainingPlan, SuccessStory, WeeklyChampion, TrainerTip

from .models import Payment
from .models import Exercise,UserExercise
from .models import ContactMessage
# Register your models here.

admin.site.register(Payment)
admin.site.register(Exercise)
admin.site.register(UserExercise )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'short_message', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)

    def short_message(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    short_message.short_description = 'الرسالة'


from django.contrib import admin
from .models import Sport, Trainer, Rating

# تسجيل نموذج الرياضة
@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# تسجيل نموذج المدرب
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'experience')
    search_fields = ('name', 'specialty__name')
    list_filter = ('specialty',)

# تسجيل نموذج التقييم
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'value', 'created_at')
    list_filter = ('value', 'created_at')
    search_fields = ('trainer__name', 'comment')




# admin.py
from django.contrib import admin
from .models import SuccessStory, WeeklyChampion, TrainerTip

@admin.register(SuccessStory)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'created_at')
    search_fields = ('name', 'quote')

@admin.register(WeeklyChampion)
class WeeklyChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'week')
    list_filter = ('week',)
    search_fields = ('name', 'achievement')

@admin.register(TrainerTip)
class TrainerTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')




from django.contrib import admin
from .models import ClubPulse

@admin.register(ClubPulse)
class ClubPulseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date', 'expire_date')
    list_filter = ('category', 'publish_date', 'expire_date')
    search_fields = ('title', 'content')



from django.contrib import admin
from .models import Sport, CoursePricing

@admin.register(CoursePricing)
class CoursePricingAdmin(admin.ModelAdmin):
    list_display = ('sport', 'base_price', 'group_training_price', 'private_training_price', 'single_session_price')
    list_filter = ('sport',)
