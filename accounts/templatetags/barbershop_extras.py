# accounts/templatetags/barbershop_extras.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def add_class(field, css_class):
    """Add CSS class to form field"""
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={"class": css_class})
    return field

@register.filter
def star_rating(rating):
    """Display star rating"""
    if not rating:
        rating = 0
    
    full_stars = int(rating)
    half_star = rating - full_stars >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    stars = []
    
    # Full stars
    for i in range(full_stars):
        stars.append('<i class="bi bi-star-fill text-warning"></i>')
    
    # Half star
    if half_star:
        stars.append('<i class="bi bi-star-half text-warning"></i>')
    
    # Empty stars
    for i in range(empty_stars):
        stars.append('<i class="bi bi-star text-muted"></i>')
    
    return mark_safe(''.join(stars))

@register.inclusion_tag('partials/booking_status_badge.html')
def booking_status_badge(status):
    """Display booking status badge"""
    return {'status': status}
