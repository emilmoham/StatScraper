from django.shortcuts import render
from django.template import loader

def index(request):
	context = {
		"message" : "Why hello there",
	}
	return render(request, 'main/index.html', context)
