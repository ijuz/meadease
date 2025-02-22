from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import SubmitPrescription
from .models import Prescriptions
from hospital.models import PatientDetails
from userApp.models import PatientModel


# def submit_prescription(request):
#     if request.method == "POST":
#         form = SubmitPrescription(request.POST)
#         if form.is_valid():
#             token = form.cleaned_data['token_number']
#             patient = PatientDetails.objects.get(token_number=token)
#             doctor = patient.doctor
#             hospital = patient.hospital


#             instance = Prescriptions.objects.create(
#                 patient=patient,
#                 doctor=doctor,
#                 hospital=hospital,
#                 text=form.cleaned_data['text']
#             )
#             instance.save()

            
#             return redirect('view_prescription')

#     else:
#         form = SubmitPrescription()
#     return render(request, 'prescription/prescription.html', {'form': form})


def view_prescription(request, pk):
    prescription = get_object_or_404(Prescriptions, pk=pk)
    context = {
        'status': "success",
        "data": {
            "patient": prescription.patient.name,
            "doctor": prescription.doctor.name,
            "hospital": prescription.hospital.name,
            "text": prescription.text,
            "date": prescription.date,
        }
    }
    return JsonResponse(context)

def submit_prescription(request):
    if request.method == "POST":
        form = SubmitPrescription(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token_number']
            patient_detail = get_object_or_404(PatientDetails, token_number=token)

            # Extract PatientModel from CustomUser
            patient = get_object_or_404(PatientModel, user=patient_detail.name)

            doctor = patient_detail.doctor  # Ensure this is a DoctorModel instance
            hospital = patient_detail.hospital  # Ensure this is a HospitalModel instance

            # Create the prescription
            instance = Prescriptions.objects.create(
                patient=patient,  # Now correctly passing a PatientModel instance
                doctor=doctor,
                hospital=hospital,
                text=form.cleaned_data['text']
            )
            instance.save()

            return redirect('view_prescription', pk=instance.pk)

    else:
        form = SubmitPrescription()
    return render(request, 'prescription/prescription.html', {'form': form})


