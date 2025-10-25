from django import forms
from .models import Patient, Symptom, Report

class PatientForm(forms.ModelForm):
    """Form for patient registration"""
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'email', 'phone', 'address', 'medical_history']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SymptomChecklistForm(forms.Form):
    """Form for selecting symptoms from a checklist"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Group symptoms by body part for better organization
        body_parts = Symptom.objects.values_list('body_part', flat=True).distinct()
        
        for body_part in body_parts:
            if not body_part:  # Skip empty body parts
                continue
                
            symptoms = Symptom.objects.filter(body_part=body_part)
            for symptom in symptoms:
                self.fields[f'symptom_{symptom.id}'] = forms.BooleanField(
                    label=symptom.name,
                    required=False,
                    help_text=symptom.description
                )
                
        # Add general symptoms (those without a specific body part)
        general_symptoms = Symptom.objects.filter(body_part__isnull=True)
        for symptom in general_symptoms:
            self.fields[f'symptom_{symptom.id}'] = forms.BooleanField(
                label=symptom.name,
                required=False,
                help_text=symptom.description
            )

class SymptomSeverityForm(forms.Form):
    """Form for rating the severity of selected symptoms"""
    def __init__(self, symptoms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for symptom in symptoms:
            self.fields[f'severity_{symptom.id}'] = forms.IntegerField(
                label=f"How severe is your {symptom.name.lower()}?",
                min_value=1,
                max_value=10,
                initial=5,
                widget=forms.NumberInput(attrs={'class': 'severity-slider', 'type': 'range'})
            )
            
            self.fields[f'duration_{symptom.id}'] = forms.ChoiceField(
                label=f"How long have you had {symptom.name.lower()}?",
                choices=[
                    ('hours', 'Hours'),
                    ('days', 'Days'),
                    ('weeks', 'Weeks'),
                    ('months', 'Months'),
                    ('years', 'Years'),
                ],
                initial='days',
            )

class ReportForm(forms.ModelForm):
    """Form for creating and editing reports"""
    class Meta:
        model = Report
        fields = ['title', 'notes', 'status']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class SymptomSearchForm(forms.Form):
    """Form for searching symptoms by keyword"""
    keyword = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search symptoms...'})
    )
    body_part = forms.ChoiceField(
        required=False,
        choices=[('', 'All Body Parts')],
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate body part choices
        body_parts = Symptom.objects.exclude(body_part__isnull=True).values_list(
            'body_part', flat=True).distinct().order_by('body_part')
        self.fields['body_part'].choices += [(bp, bp) for bp in body_parts]