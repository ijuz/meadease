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

            # Create a new prescription instance and save it
            instance = Prescriptions.objects.create(
                patient=patient,
                doctor=doctor,
                hospital=hospital,
                text=form.cleaned_data['text']
            )
            instance.save()

            # Clear the form by creating a new instance
            form = SubmitPrescription()  # Reset the form to an empty instance

            # Redirect to view the prescription
            return redirect('view_prescription', id=instance.id)

    else:
        form = SubmitPrescription()  # Initialize an empty form
    return render(request, 'prescription/prescription.html', {'form': form})


def view_prescription(request, id):
    prescription = get_object_or_404(Prescriptions, id=id)
    return render(request, 'view_prescription.html', {'pris': prescription})


def create_prescription(request):
    patient_name = None  # Initialize a variable to hold the patient's name

    if request.method == "POST":
        form = SubmitPrescription(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token_number']
            # Get the patient based on the token number
            patient = get_object_or_404(PatientDetails, token_number=token)
            patient_name = patient.full_name  # Fetch the patient's name

            # Create a prescription instance for the patient
            pris = form.save(commit=False)
            pris.patient = patient  # Associate the patient with the prescription
            pris.save()

            # Redirect to the view after successful form submission
            return redirect('view_prescription', id=pris.id)

    else:
        form = SubmitPrescription()

    return render(request, 'prescription_form.html', {'form': form, 'patient_name': patient_name})
