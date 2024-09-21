
from django.urls import path,include
from . import extract_views

urlpatterns = [


    path('offres/public/linkedin', extract_views.linkedin_jobs, name='linkedin_offres'),
    path('offres/public/keejob', extract_views.keejob_jobs, name='keejob_jobs'),
    path('offres/public/optioncarrier', extract_views.open, name='optioncarriere_jobs'),


]
