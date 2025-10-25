from django.db import models
from django.utils import timezone
import uuid

class Patient(models.Model):
    """Model for storing patient information"""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.age})"

class Symptom(models.Model):
    """Model for storing symptoms"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    severity_level = models.PositiveIntegerField(default=1)  # 1-10 scale
    body_part = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Disease(models.Model):
    """Model for storing diseases"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    symptoms = models.ManyToManyField(Symptom, related_name='diseases')
    severity_level = models.PositiveIntegerField(default=1)  # 1-10 scale
    common_age_group = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Remedy(models.Model):
    """Model for storing natural remedies and yoga practices"""
    TYPE_CHOICES = (
        ('NATURAL', 'Natural Remedy'),
        ('YOGA', 'Yoga Practice'),
        ('DIET', 'Dietary Recommendation'),
        ('LIFESTYLE', 'Lifestyle Change'),
    )
    
    name = models.CharField(max_length=100)
    remedy_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    instructions = models.TextField()
    diseases = models.ManyToManyField(Disease, related_name='remedies', blank=True)
    symptoms = models.ManyToManyField(Symptom, related_name='remedies', blank=True)
    contraindications = models.TextField(blank=True, null=True)
    effectiveness_rating = models.PositiveIntegerField(default=1)  # 1-5 scale
    
    def __str__(self):
        return f"{self.name} ({self.get_remedy_type_display()})"
    
    class Meta:
        verbose_name_plural = "Remedies"

class Report(models.Model):
    """Model for storing patient health reports"""
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('COMPLETED', 'Completed'),
        ('SHARED', 'Shared'),
    )
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=200)
    symptoms = models.ManyToManyField(Symptom, related_name='reports')
    predicted_diseases = models.ManyToManyField(Disease, related_name='reports', blank=True)
    recommended_remedies = models.ManyToManyField(Remedy, related_name='reports', blank=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Report for {self.patient.name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_share_url(self):
        """Generate a shareable URL for the report"""
        return f"/reports/{self.uuid}/"
    
    def export_to_pdf(self):
        """Method to export report to PDF format"""
        # Implementation will be added later
        pass
