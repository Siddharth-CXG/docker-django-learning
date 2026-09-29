from django.http import JsonResponse
from django.shortcuts import render

from .forms import ContactMessageForm


def home(request):
	statistics = [
		{'label': 'Total Assets', 'value': 4},
		{'label': 'Active Assets', 'value': 3},
		{'label': 'Alerts', 'value': 1},
	]
	return render(request, 'dashboard/home.html', {'statistics': statistics})


def assets(request):
	asset_list = [
		{'name': 'Sunrise Solar Array', 'type': 'Solar PV', 'status': 'Active'},
		{'name': 'North Ridge Wind Farm', 'type': 'Wind', 'status': 'Active'},
		{'name': 'Harbor Battery', 'type': 'Battery Storage', 'status': 'Active'},
		{'name': 'East Field Solar', 'type': 'Solar PV', 'status': 'Maintenance'},
	]
	return render(request, 'dashboard/assets.html', {'assets': asset_list})


def about(request):
	return render(request, 'dashboard/about.html')


def contact(request):
	submitted = False
	if request.method == 'POST':
		form = ContactMessageForm(request.POST)
		if form.is_valid():
			form.save()
			form = ContactMessageForm()
			submitted = True
	else:
		form = ContactMessageForm()
	return render(request, 'dashboard/contact.html', {'form': form, 'submitted': submitted})


def health(request):
	return JsonResponse({'status': 'healthy'})


def placeholder(request, page_title):
    return render(request, 'dashboard/placeholder.html', {'page_title': page_title})
