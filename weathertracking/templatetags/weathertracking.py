from math import pi
from django import template
from django.contrib.gis.measure import D

register = template.Library()

@register.filter(name='m_to_ft')
def m_to_ft(value):
    "Converts the value into feet from meters."
    if value:
        return D(meter=value).survey_ft
    else:
        return None

@register.filter(name='rad_to_deg')
def rad_to_deg(value):
    "Converts the value into degrees from radians."
    if value:
        return float(value) * 180 / pi
    else:
        return None
