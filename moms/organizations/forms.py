from django import forms
from .models import Organization, CustomUser, Role
from django.contrib.auth.forms import AuthenticationForm

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'address','orgown']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'organization', 'role']
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role']  # Exclude username, auto-assigned

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        # Ensure 'role' is in the fields before applying queryset
        if 'role' in self.fields:
            self.fields['role'].queryset = Role.objects.exclude(name__iexact="super_admin")
            print(self.fields['role'].queryset)  # Debug: Check filtered queryset in console


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role']  # Editors can't edit roles

    def __init__(self, *args, **kwargs):
            super(UserEditForm, self).__init__(*args, **kwargs)
            print(Role.objects.exclude(name="super_admin"))
            # Exclude "super admin" from the role dropdown
            self.fields['role'].queryset = Role.objects.exclude(name="super_admin")
