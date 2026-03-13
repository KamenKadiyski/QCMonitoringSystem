from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=100)
    qc_sample_is_required = models.BooleanField(default=False)

class DeliveryQualityIssue(models.Model):
    supplier=models.ForeignKey(Supplier, on_delete=models.CASCADE,related_name='delivery_quality_issues')
    material=models.ForeignKey('materials.Material',
                               on_delete=models.SET_NULL,blank=True,null=True,
                               related_name='material_quality_issues')
    additive=models.ForeignKey('materials.Additive',
                               on_delete=models.SET_NULL,blank=True,null=True,
                               related_name='additive_quality_issues')
    issue_description=models.TextField()
    bach_number=models.CharField(max_length=100,blank=True,null=True)
    issue_date=models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.material and not self.additive:
            raise ValidationError("Either material or additive must be specified.")
        if self.material and self.additive:
            raise ValidationError("Only one of material or additive can be specified.")

    def __str__(self):
        item= self.material.name if self.material else self.additive.name
        return f"{self.issue_date} - {item} - {self.supplier.name}"






class Customer(models.Model):
    name = models.CharField(max_length=100)
    customer_own_labeling=models.BooleanField(default=False)