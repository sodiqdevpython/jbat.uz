from django import template

register = template.Library()

@register.filter
def phone_number(val):
    val = f"+998 {val[0:2]} {val[2:5]} {val[5:7]} {val[7:9]}"
    return val