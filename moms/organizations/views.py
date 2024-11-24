
from django.contrib.auth import  login
from .forms import CustomLoginForm
from .models import Organization
from .forms import OrganizationForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Role
from .forms import UserCreationForm, UserEditForm
from django.shortcuts import render, redirect
from .forms import UserCreationForm
from .models import Role
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Organization


def custom_login(request):
    if request.user.is_authenticated:

        if request.user.role.name == 'super_admin':
            return redirect('super_admin_dashboard')
        else:
             return redirect('user_list')

    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('super_admin_dashboard') 
        
    else:
        form = CustomLoginForm()

    return render(request, 'organizations/login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')



@login_required
def organization_list(request):
    organizations = Organization.objects.all()
    return render(request, 'organizations/organization_list.html', {'organizations': organizations})

@login_required
def assign_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id, organization=request.user.organization)
    if not request.user.role.name== 'admin':  
        messages.error(request, "Only Admin Can Assign Role.")

    if request.method == 'POST':
        role = request.POST.get('role')
        user.role= role
        user.save()
        return redirect('user_list')

    roles = Role.objects.all()
    return render(request, 'organizations/assign_role.html', {'user': user, 'roles': roles})





@login_required
def super_admin_dashboard(request):
   
    if request.user.role.name != 'super_admin':
        return redirect('user_list') 

    organizations = Organization.objects.prefetch_related(
        'users'
    ) 

    organization_data = []
    for org in organizations:
        admin_user = org.users.filter(role__name__in=['admin', 'super_admin']).first() # Get admin user if exists
        organization_data.append({
            'id': org.id,
            'name': org.name,
            'address':org.address,
            'orgown':org.orgown,
            'admin_username': admin_user.username if admin_user else None,
        })
      
    return render(request, 'organizations/super_admin_dashboard.html', {'organizations': organization_data})


@login_required
def create_organization(request):

    if request.user.role.name!= 'super_admin':
        messages.error(request, "Only Super Admin Can Create Organization.")

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():

            organization = form.save()
            admin_role = Role.objects.get(name='admin')
            admin_user = CustomUser(
                username=f"org_{organization.id:04d}_0001",  
                email=f"admin@{organization.name.lower().replace(' ', '')}.com", 
                role=admin_role,
                organization=organization
            )
            admin_user.set_password('12345')
            admin_user.is_staff = False  
            admin_user.save()
            return redirect('super_admin_dashboard')
        else:
            messages.error(request, "Invalid Form Data.")
    else:

        form = OrganizationForm()

    return render(request, 'organizations/create_organization.html', {'form': form})



@login_required
def edit_organization(request, org_id):
    if request.user.role.name!= 'super_admin':
         messages.error(request, "Only Super Admin Can Edit Organization.")

    organization = Organization.objects.get(id=org_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('super_admin_dashboard')

    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'organizations/edit_organization.html', {'form': form, 'organization': organization})



@login_required
def delete_organization(request, org_id):
    org_to_delete = get_object_or_404(Organization, id=org_id)
    
   
    if org_to_delete.name == "Admin Organization":
        messages.error(request, "Admin Organization cannot be deleted.")
        return redirect('super_admin_dashboard')
    if request.user.role.name!= 'super_admin':
        return redirect('home')

    organization = Organization.objects.get(id=org_id)
    organization.delete()
    return redirect('super_admin_dashboard')



@login_required
def create_user(request):
    roles = Role.objects.exclude(name__in=["super_admin",'admin'])
    if request.user.role.name!= 'admin':
         messages.error(request, "Only Admin Can Create User.")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        user_org = request.user.organization

        user_in_org =CustomUser.objects.filter(organization=user_org).count() + 1

        if form.is_valid():

            user = form.save(commit=False)
            user.organization = user_org
            user.username = f"{user_org.name}_user_{user_in_org}"
            user.email = f"user{user_in_org}@{user_org.name.lower().replace(' ', '')}.com"
            user.set_password("12345")  
            user.save()
            return redirect('user_list')
    else:
        form = UserCreationForm()
    return render(request, 'organizations/create_user.html', {'form': form, 'roles': roles})

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    filter_out_role = ['super_admin']
    if user.role.name != 'admin':
        filter_out_role.append('admin')

    roles = Role.objects.exclude(name__in=filter_out_role)
    if request.user.role.name!= 'admin' and user.role.name == 'admin':
        messages.error(request, "Only Admin Can Edit User.")
        return redirect('/') 


    if user.organization != request.user.organization:
        return redirect('/') 

    if request.user.role.name not in ['admin', 'edit']:
        return redirect('/') 
    new_role = request.POST.get("role")

    if request.user.role.name == "edit" and new_role == "2":
        messages.error(request, "Users with 'edit' role cannot assign 'admin' role.")
        return redirect('/') 

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        print(form)
        if form.is_valid():
            if request.user.role.name == 'edit':
                form.cleaned_data.pop('role', None)  
            user = form.save(commit=False)
            user.save()
            return redirect('user_list')
        else:
            messages.error(request,'Invalid form data')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'organizations/edit_user.html', {'form': form, 'user': user,'roles':roles})



@login_required
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(CustomUser, id=user_id)
    print(user_to_delete.username,request.user.username)
    if user_to_delete.username == request.user.username:
        messages.error(request,'User CanNot Delete self')
        return redirect('user_list')
    if request.user.role.name == 'edit':
        messages.error(request,'Access Denied')
        return redirect('user_list')
    if user_to_delete.role.name.lower() == "admin":
        if request.user.role.name.lower() != "super_admin":
            messages.error(request, "Only Super Admin can delete an Admin.")
            return redirect('user_list')

        if Organization.objects.filter(admin=user_to_delete).exists():
            messages.error(request, "Admin cannot be deleted while they are associated with an organization. Please remove the organization first.")
            return redirect('user_list')
        if request.user.role.name != 'admin' or user_to_delete.organization != request.user.organization:
         messages.error(request,'Only admins can delete users in their organization')


    user_to_delete.delete()
    messages.success(request, f"User {user_to_delete.first_name} {user_to_delete.last_name} deleted successfully.")
    return redirect('user_list')


@login_required
def user_list(request):
    users = CustomUser.objects.filter(organization=request.user.organization)
    role_view =False if request.user.role.name == 'view' else True 
    return render(request, 'organizations/user_list.html', {'users': users,'role_view':role_view})
