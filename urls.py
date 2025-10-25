from django.urls import path
from . import views

app_name = 'health_predictor'

urlpatterns = [
    # Home page
    path('', views.HomeView.as_view(), name='home'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Patient URLs
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/new/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    
    # Symptom checker URLs
    path('symptom-checker/', views.SymptomCheckerView.as_view(), name='symptom_checker'),
    path('symptom-checker/<int:patient_id>/', views.SymptomCheckerView.as_view(), name='symptom_checker'),
    path('symptom-severity/', views.SymptomSeverityView.as_view(), name='symptom_severity'),
    path('symptom-severity/<int:patient_id>/', views.SymptomSeverityView.as_view(), name='symptom_severity'),
    path('prediction-results/', views.PredictionResultsView.as_view(), name='prediction_results'),
    path('prediction-results/<int:patient_id>/', views.PredictionResultsView.as_view(), name='prediction_results'),
    
    # Report URLs
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/shared/<uuid:uuid>/', views.ReportDetailView.as_view(), name='report_shared'),
    path('reports/<int:pk>/edit/', views.ReportUpdateView.as_view(), name='report_update'),
    path('reports/<int:pk>/share/', views.ReportShareView.as_view(), name='report_share'),
    path('reports/<int:pk>/export/<str:format>/', views.ReportExportView.as_view(), name='report_export'),
    
    # API endpoints
    path('api/symptoms/search/', views.SymptomSearchAPIView.as_view(), name='api_symptom_search'),
]