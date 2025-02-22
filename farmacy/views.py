from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import PharmacyForm
from .models import Pharmacy
from django.http import JsonResponse
from .scanner import scan_qr_code


def Pharmacy_register(request):
    if request.method == 'POST':
        form = PharmacyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard-view")
    else:
        form = PharmacyForm()
    context={
        "form":form
    }
    return render(request,'pharmacy/index.html',context=context)


def get_link(request):
    get_user = Pharmacy.objects.all()
    

def sent_data(request):
    if request.method == 'POST':
        qr_data = scan_qr_code()  # Get QR code data
        print("QR Code Data:", qr_data)
        
        return render(request, 'scanqr/index.html', {'qr_data': qr_data})

    return render(request, 'scanqr/index.html', {'error': 'Invalid request method'})