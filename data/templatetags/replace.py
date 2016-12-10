from django import template
register = template.Library()

@register.filter
def changePercent(value):
	return value.replace('%','_')

@register.filter
def changeSpace(value):
    return value.replace(' ', '_')

@register.filter
def scrub(value):
    value = value.replace(';','9')
    value = value.replace('&','8')
    value = value.replace('(','7')
    value = value.replace(')','6')
    value = value.replace(' ','_')
    value = value.replace('\'','5')
    return value
