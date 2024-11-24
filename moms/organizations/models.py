from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='users')
    role =  models.ForeignKey('Role', on_delete=models.CASCADE, related_name='role')
       
    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if update_fields and 'last_login' in update_fields:
            super().save(*args, **kwargs)
            return
        
        if self.role.name == "super_admin" :
            raise ValidationError("Only one super_admin is allowed.")
        if self.role.name == 'admin' and CustomUser.objects.filter(organization=self.organization,role=self.role).exists():
            raise ValidationError('Only one Admin allowed for one organizations.')
        if not self.pk: 
            org_count = CustomUser.objects.filter(organization=self.organization).count() + 1
            self.username = f"org_{self.organization.id:04d}_{org_count:04d}" 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class Organization(models.Model):
    name = models.CharField(max_length=255,unique=True)
    address = models.TextField(blank=True, null=True)
    orgown =models.CharField(max_length=20)
    is_main = models.BooleanField(default=False) 
    
    def save(self, *args, **kwargs):
        
        if self.is_main:
                raise ValidationError('There Can be only one main Orgainzations.')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_main:
            raise ValidationError("The Admin Organization cannot be deleted.")
        super().delete(*args, **kwargs)
    

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50)  
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
