from django.db import models
from django.utils.translation import gettext_lazy as _


class Postulation(models.Model):
    id = models.AutoField(primary_key=True)  # Maps to the AUTO generation of id
    date_postulation = models.DateField()  # LocalDate equivalent in Django
    decision_recruteur = models.CharField(max_length=255)  # String field

    # Mapping the foreign keys with File model
    cv = models.OneToOneField(
        'File', 
        on_delete=models.CASCADE, 
        related_name='cv_postulation'
    )
    
    lettre_motivation = models.OneToOneField(
        'File', 
        on_delete=models.CASCADE, 
        related_name='lettre_postulation'
    )

class Meta:
    db_table = 'postulation'  # This maps to the existing table created by another microservice
    managed = False  # This tells Django not to try to manage the schema (no migrations)
class File(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file_data = models.BinaryField()  # Assuming you store binary data

    class Meta:
        db_table = 'file'

class OffresPublic(models.Model):
    class Meta:
        db_table = 'offres'  # Specify the actual table name here
        managed = False  # Prevent Django from managing the schema

    titre = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField(blank=True, null=True)
    company = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    sector = models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=255,null=True)
    availability = models.CharField(max_length=255,null=True)
    description= models.CharField(max_length=255,null=True)
    type= models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.title
