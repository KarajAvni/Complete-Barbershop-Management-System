# barbershop_project/context_processors.py
from shop.models import ShopSettings

def shop_settings(request):
    """Add shop settings to template context"""
    try:
        settings = ShopSettings.objects.first()
        return {'shop_settings': settings}
    except ShopSettings.DoesNotExist:
        return {'shop_settings': None}