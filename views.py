from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, FileResponse
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Patient, Symptom, Disease, Remedy, Report
from .forms import PatientForm, SymptomChecklistForm, SymptomSeverityForm, ReportForm, SymptomSearchForm

import json
import io
import csv
import uuid
import datetime

# Home view
class HomeView(View):
    def get(self, request):
        return render(request, 'health_predictor/home.html')

# Dashboard view
class DashboardView(View):
    def get(self, request):
        # Get counts for dashboard metrics
        patient_count = Patient.objects.count()
        report_count = Report.objects.count()
        symptom_count = Symptom.objects.count()
        
        # Get recent reports
        recent_reports = Report.objects.select_related('patient').order_by('-created_at')[:5]
        
        # Get common diseases
        common_diseases = Disease.objects.annotate(count=Count('reports')).order_by('-count')[:5]
        
        # Generate chart data for the last 7 days
        today = timezone.now().date()
        date_labels = [(today - datetime.timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
        
        # Count reports for each day
        report_data = []
        for i in range(6, -1, -1):
            date = today - datetime.timedelta(days=i)
            count = Report.objects.filter(
                created_at__year=date.year,
                created_at__month=date.month,
                created_at__day=date.day
            ).count()
            report_data.append(count)
        
        context = {
            'patient_count': patient_count,
            'report_count': report_count,
            'symptom_count': symptom_count,
            'recent_reports': recent_reports,
            'common_diseases': common_diseases,
            'chart_labels': json.dumps(date_labels),
            'chart_data': json.dumps(report_data)
        }
        
        return render(request, 'health_predictor/dashboard.html', context)

# Patient views
class PatientListView(ListView):
    model = Patient
    template_name = 'health_predictor/patient_list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']
    paginate_by = 10

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'health_predictor/patient_detail.html'
    context_object_name = 'patient'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = self.object.reports.all().order_by('-created_at')
        return context

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'health_predictor/patient_form.html'
    
    def get_success_url(self):
        return reverse('health_predictor:patient_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.name} created successfully!")
        return super().form_valid(form)

class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'health_predictor/patient_form.html'
    
    def get_success_url(self):
        return reverse('health_predictor:patient_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance.name} updated successfully!")
        return super().form_valid(form)

# Symptom analysis and disease prediction views
class SymptomCheckerView(View):
    def get(self, request, patient_id=None):
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        
        symptom_form = SymptomChecklistForm()
        search_form = SymptomSearchForm()
        
        return render(request, 'health_predictor/symptom_checker.html', {
            'patient': patient,
            'symptom_form': symptom_form,
            'search_form': search_form,
        })
    
    def post(self, request, patient_id=None):
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        
        form = SymptomChecklistForm(request.POST)
        if form.is_valid():
            # Extract selected symptoms
            selected_symptoms = []
            for field_name, value in form.cleaned_data.items():
                if field_name.startswith('symptom_') and value:
                    symptom_id = int(field_name.split('_')[1])
                    selected_symptoms.append(symptom_id)
            
            if not selected_symptoms:
                messages.warning(request, "Please select at least one symptom.")
                return redirect('health_predictor:symptom_checker', patient_id=patient_id)
            
            # Store selected symptoms in session
            request.session['selected_symptoms'] = selected_symptoms
            
            # Redirect to severity assessment
            if patient_id:
                return redirect('health_predictor:symptom_severity', patient_id=patient_id)
            else:
                return redirect('health_predictor:symptom_severity')
        
        return render(request, 'health_predictor/symptom_checker.html', {
            'patient': patient,
            'symptom_form': form,
            'search_form': SymptomSearchForm(),
        })

class SymptomSeverityView(View):
    def get(self, request, patient_id=None):
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        
        # Get selected symptoms from session
        selected_symptom_ids = request.session.get('selected_symptoms', [])
        if not selected_symptom_ids:
            messages.warning(request, "Please select symptoms first.")
            return redirect('health_predictor:symptom_checker', patient_id=patient_id)
        
        selected_symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)
        severity_form = SymptomSeverityForm(symptoms=selected_symptoms)
        
        return render(request, 'health_predictor/symptom_severity.html', {
            'patient': patient,
            'severity_form': severity_form,
            'symptoms': selected_symptoms,
        })
    
    def post(self, request, patient_id=None):
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        
        # Get selected symptoms from session
        selected_symptom_ids = request.session.get('selected_symptoms', [])
        if not selected_symptom_ids:
            messages.warning(request, "Please select symptoms first.")
            return redirect('health_predictor:symptom_checker', patient_id=patient_id)
        
        selected_symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)
        form = SymptomSeverityForm(symptoms=selected_symptoms, data=request.POST)
        
        if form.is_valid():
            # Process symptom severity data
            symptom_data = {}
            for symptom in selected_symptoms:
                severity = form.cleaned_data.get(f'severity_{symptom.id}', 5)
                duration = form.cleaned_data.get(f'duration_{symptom.id}', 'days')
                symptom_data[symptom.id] = {
                    'severity': severity,
                    'duration': duration,
                }
            
            # Store symptom data in session
            request.session['symptom_data'] = symptom_data
            
            # Redirect to results
            if patient_id:
                return redirect('health_predictor:prediction_results', patient_id=patient_id)
            else:
                return redirect('health_predictor:prediction_results')
        
        return render(request, 'health_predictor/symptom_severity.html', {
            'patient': patient,
            'severity_form': form,
            'symptoms': selected_symptoms,
        })

class PredictionResultsView(View):
    def get(self, request, patient_id=None):
        patient = None
        if patient_id:
            patient = get_object_or_404(Patient, id=patient_id)
        
        # Get selected symptoms and their data from session
        selected_symptom_ids = request.session.get('selected_symptoms', [])
        symptom_data = request.session.get('symptom_data', {})
        
        if not selected_symptom_ids or not symptom_data:
            messages.warning(request, "Please complete the symptom assessment first.")
            return redirect('health_predictor:symptom_checker', patient_id=patient_id)
        
        # Get the selected symptoms
        symptoms = Symptom.objects.filter(id__in=selected_symptom_ids)
        
        # Predict diseases based on symptoms
        # This is a simple implementation. In a real-world scenario, you would use a more sophisticated algorithm.
        predicted_diseases = Disease.objects.filter(symptoms__in=symptoms).annotate(
            symptom_count=Count('symptoms', filter=Q(symptoms__in=symptoms))
        ).order_by('-symptom_count', '-severity_level')[:5]
        
        # Get recommended remedies for the predicted diseases and symptoms
        recommended_remedies = Remedy.objects.filter(
            Q(diseases__in=predicted_diseases) | Q(symptoms__in=symptoms)
        ).distinct().order_by('-effectiveness_rating')
        
        # Create a new report if patient exists
        report = None
        if patient:
            report = Report.objects.create(
                patient=patient,
                title=f"Health Report - {timezone.now().strftime('%Y-%m-%d')}",
                status='DRAFT'
            )
            report.symptoms.set(symptoms)
            report.predicted_diseases.set(predicted_diseases)
            report.recommended_remedies.set(recommended_remedies)
            report.save()
        
        context = {
            'patient': patient,
            'symptoms': symptoms,
            'symptom_data': symptom_data,
            'predicted_diseases': predicted_diseases,
            'recommended_remedies': recommended_remedies,
            'report': report,
        }
        
        return render(request, 'health_predictor/prediction_results.html', context)

# Report views
class ReportDetailView(DetailView):
    model = Report
    template_name = 'health_predictor/report_detail.html'
    context_object_name = 'report'
    
    def get_object(self, queryset=None):
        # Allow retrieval by UUID for sharing
        uuid_string = self.kwargs.get('uuid')
        if uuid_string:
            return get_object_or_404(Report, uuid=uuid_string)
        return super().get_object(queryset)

class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'health_predictor/report_form.html'
    
    def get_success_url(self):
        return reverse('health_predictor:report_detail', kwargs={'pk': self.object.pk})

class ReportShareView(View):
    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.status = 'SHARED'
        report.save()
        
        share_url = request.build_absolute_uri(
            reverse('health_predictor:report_shared', kwargs={'uuid': report.uuid})
        )
        
        return render(request, 'health_predictor/report_share.html', {
            'report': report,
            'share_url': share_url,
        })

class ReportExportView(View):
    def get(self, request, pk, format='pdf'):
        report = get_object_or_404(Report, pk=pk)
        
        if format == 'pdf':
            # Implementation for PDF export will be added later
            # For now, we'll return a simple text response
            return HttpResponse("PDF export functionality will be implemented soon.")
        
        elif format == 'csv':
            # Create CSV file
            buffer = io.StringIO()
            writer = csv.writer(buffer)
            
            # Write header
            writer.writerow(['Health Report', report.title])
            writer.writerow(['Patient', report.patient.name])
            writer.writerow(['Date', report.created_at.strftime('%Y-%m-%d')])
            writer.writerow([])
            
            # Write symptoms
            writer.writerow(['Symptoms'])
            for symptom in report.symptoms.all():
                writer.writerow([symptom.name, symptom.description])
            writer.writerow([])
            
            # Write predicted diseases
            writer.writerow(['Predicted Conditions'])
            for disease in report.predicted_diseases.all():
                writer.writerow([disease.name, disease.description])
            writer.writerow([])
            
            # Write recommended remedies
            writer.writerow(['Recommended Remedies'])
            for remedy in report.recommended_remedies.all():
                writer.writerow([remedy.name, remedy.get_remedy_type_display(), remedy.description])
            
            # Create response
            buffer.seek(0)
            response = HttpResponse(buffer.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="health_report_{report.uuid}.csv"'
            
            return response
        
        else:
            return HttpResponse("Unsupported export format", status=400)

# API endpoints for AJAX requests
class SymptomSearchAPIView(View):
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        body_part = request.GET.get('body_part', '')
        
        symptoms = Symptom.objects.all()
        
        if keyword:
            symptoms = symptoms.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
        
        if body_part:
            symptoms = symptoms.filter(body_part=body_part)
        
        data = [{
            'id': symptom.id,
            'name': symptom.name,
            'description': symptom.description,
            'body_part': symptom.body_part or 'General',
            'severity_level': symptom.severity_level,
        } for symptom in symptoms[:20]]  # Limit to 20 results
        
        return JsonResponse({'symptoms': data})
