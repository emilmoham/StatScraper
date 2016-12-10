from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter
def get_float_item(dictionary, key):
	return float(dictionary.get(key))
