from .models import SportPricing
import uuid

from decimal import Decimal

def calculate_plan_price(plan):
    # التحقق من وجود بيانات التسعير
    try:
        pricing = SportPricing.objects.get(
            sport_name=plan.activity,
            session_type=plan.training_type
        )
        base_price = pricing.price
    except SportPricing.DoesNotExist:
        base_price = Decimal('0.00')

    # تعديل السعر حسب مدة الخطة
    duration_multiplier = {
        'session': 1,
        'week': 5,
        'month': 20,
        '3_months': 50,
        'custom': 10  # قيمة افتراضية
    }

    multiplier = duration_multiplier.get(plan.duration, 1)
    final_price = base_price * Decimal(multiplier)

    # تأكيد أن السعر لا يقل عن الحد الأدنى
    return max(final_price, Decimal('10.00'))

def generate_transaction_id():
    return str(uuid.uuid4())

def process_payment(payment):
    # محاكاة الدفع: دائماً ناجح
    return True
