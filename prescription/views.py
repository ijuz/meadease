from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import SubmitPrescription
from .models import Prescriptions
from hospital.models import PatientDetails


def submit_prescription(request):
    if request.method == "POST":
        form = SubmitPrescription(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token_number']
            patient = PatientDetails.objects.get(token_number=token)
            doctor = patient.doctor
            hospital = patient.hospital


            instance = Prescriptions.objects.create(
                patient=patient,
                doctor=doctor,
                hospital=hospital,
                text=form.cleaned_data['text']
            )
            instance.save()

            
            return redirect('view_prescription')

    else:
        form = SubmitPrescription()
    return render(request, 'prescription/prescription.html', {'form': form})


# def submit_prescription(request):
#     if request.method == "POST":
#         form = SubmitPrescription(request.POST)
#         if form.is_valid():
#             token = form.cleaned_data['token_number']
#             patient = get_object_or_404(PatientDetails, token_number=token)
#             doctor = patient.doctor
#             hospital = patient.hospital

#             # Create the Prescription instance
#             prescription = Prescriptions.objects.create(
#                 patient=patient,
#                 doctor=doctor,
#                 hospital=hospital,
#                 text=form.cleaned_data['text'],
#                 symptoms=form.cleaned_data['symptoms'],
#                 diagnosis=form.cleaned_data['diagnosis'],
#                 additional_notes=form.cleaned_data['additional_notes'],
#                 doctor_signature=form.cleaned_data['doctor_signature']
#             )

#             # Saving medicines if available
#             medicine_names = request.POST.getlist('medicine_name')
#             dosages = request.POST.getlist('dosage')
#             forms = request.POST.getlist('form')
#             quantities = request.POST.getlist('quantity')
#             instructions = request.POST.getlist('instructions')

#             for i in range(len(medicine_names)):
#                 if medicine_names[i].strip():  # Avoid saving empty medicine fields
#                     Medicine.objects.create(
#                         prescription=prescription,
#                         name=medicine_names[i],
#                         dosage=dosages[i],
#                         form=forms[i],
#                         quantity=quantities[i],
#                         instructions=instructions[i]
#                     )

#             return redirect('view_prescription', pk=prescription.pk)

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

def create_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_prescription')  # Redirect after successful form submission
    else:
        form = PrescriptionForm()
    
    return render(request, 'prescription_form.html', {'form': form})


