from django.shortcuts import render
from .forms import DeviceForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic.logic_device import create_device, get_devices, get_deviceSede
from sites.logic.site_logic import get_site_by_name
import requests
import datetime
import json



def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__
    
def device_list(request):
    role = requests.post("http://10.128.0.7:8080/getRole/", headers={"Accept":"application/json"}, json=json.dumps(request.user.social_auth.get(provider="auth0"), default=json_default, sort_keys=True, indent=4)).text
    if role == "Medico":
        context = {
            'device_list': []
        }
        return render(request, 'Device/devices.html', context)
    else:
        return HttpResponse("Unauthorized User")

def device_list_(request):
    devices = get_devices()
    context = {
        'device_list': devices
    }
    return render(request, 'Device/devices.html', context)


def getSede(request):
    if request.method == 'GET':
        sede = request.GET.get('sede')
        sede = get_site_by_name(sede)
        devices = []
        if sede is not None:
            devices = get_deviceSede(sede.id)
        
    context = {
        'device_list': devices,
        'sede': sede
    }
    return render(request, 'Device/devices.html', context)

def device_create1(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            create_device(form)
            messages.add_message(request, messages.SUCCESS, 'Device create successful')
            return HttpResponseRedirect(reverse('devices:deviceCreate'))
        else:
            print(form.errors)
    else:
        form = DeviceForm()

    context = {
        'form': form,
    }

    return render(request, 'Device/deviceCreate.html', context)

# MICROSERVICIO
@csrf_exempt
def device_create(request):
    if request.method == 'POST':
        print(request.POST)
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save()
            return JsonResponse({'status': 'success', 'device_id': device.id})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'}, status=405)
