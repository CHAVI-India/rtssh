
from django.db import models

# TG263 Table 
class TG263Data(models.Model):
    id = models.AutoField(primary_key=True)
    Target_Type = models.CharField(max_length=255)
    Major_Category = models.CharField(max_length=255)
    Minor_Category = models.CharField(max_length=255)
    Anatomic_Group = models.CharField(max_length=255)
    TG263_Primary_Name = models.CharField(max_length=255, unique=True)
    TG263_Reverse_Order_Name = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    FMAID = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'TG263 Data'
        verbose_name_plural = 'TG263 Data'

    def __str__(self):
        return f"{self.TG263_Primary_Name} | {self.Description}"


# Label Mapping Table
class LabelMapping(models.Model):
    label_id = models.AutoField(primary_key=True)
    TG263_Primary_Name = models.ForeignKey(
        TG263Data,
        on_delete=models.CASCADE,
        to_field="TG263_Primary_Name",  # This line specifies the field to use as the foreign key
    )
    original_label = models.CharField(max_length=255)
    TG263_label = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Label Mapping'
        verbose_name_plural = 'Label Mapping'

    def __str__(self):
        return f"{self.original_label} -> {self.TG263_label}"

    def save(self, *args, **kwargs):
        self.TG263_label = self.TG263_Primary_Name.TG263_Primary_Name
        super().save(*args, **kwargs)

    
# Upload File and it will store the uploaded files in the 'uploads' folder
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  
    class Meta:
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded File'

# Preprocess File and it will store the processed files in the 'downloads' folder
class ProcessedFile(models.Model):
    file = models.FileField(upload_to='downloads/')  
    class Meta:
        verbose_name = 'Processed File'
        verbose_name_plural = 'Processed File'


