from django.db import models

from billing.models import BillingProfile
BILLING_TYPES=(
  ('billing','Billing'),
  ('shipping','Shipping'),
)
COUNTRY_TYPES=(
('india','India'),
)
STATE_TYPES=(
  ('uttar pradesh','Uttar Pradesh'),
  ('delhi','Delhi'),
)
DISTT_TYPES=(
('pratapgarh','Pratapgarh'),
('allahabad','Allahabad'),
('lucknow','Lucknow'),
('kanpur','Kanpur'),
('new delhi','New Delhi'),
)
class AddressModel(models.Model):
    billing_profile=models.ForeignKey(BillingProfile,on_delete=models.CASCADE,related_name='address_model',null=True,blank=True)
    address_type=models.CharField(max_length=20,choices=BILLING_TYPES)
    address_line_1=models.CharField(max_length=150)
    address_line_2=models.CharField(max_length=150,null=True,blank=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,choices=STATE_TYPES)
    district=models.CharField(max_length=40,choices=DISTT_TYPES)
    country=models.CharField(max_length=50,choices=COUNTRY_TYPES)
    postal_code=models.CharField(max_length=6)


    def __str__(self):
        return str(self.billing_profile)
