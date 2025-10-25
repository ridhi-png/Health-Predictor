from django.contrib import admin
from .models import Patient, Symptom, Disease, Remedy, Report

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('gender', 'created_at')

@admin.register(Symptom)
class SymptomAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity_level', 'body_part')
    search_fields = ('name', 'description')
    list_filter = ('severity_level', 'body_part')

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'severity_level', 'common_age_group')
    search_fields = ('name', 'description')
    list_filter = ('severity_level',)
    filter_horizontal = ('symptoms',)

@admin.register(Remedy)
class RemedyAdmin(admin.ModelAdmin):
    list_display = ('name', 'remedy_type', 'effectiveness_rating')
    search_fields = ('name', 'description')
    list_filter = ('remedy_type', 'effectiveness_rating')
    filter_horizontal = ('diseases', 'symptoms')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'status', 'created_at')
    search_fields = ('title', 'patient__name')
    list_filter = ('status', 'created_at')
    readonly_fields = ('uuid',)
    filter_horizontal = ('symptoms', 'predicted_diseases', 'recommended_remedies')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient')
