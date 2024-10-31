from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Organizations, Regions, Districts, RoomsEquipment
from accounts.forms import UpdateProfileForm
from django.db.models import Q, Count
from .forms import UpdateOrganizationForm, CreateOrganizationForm
from django.utils import timezone
from datetime import timedelta


@login_required
def dashboard(request):
    if request.user.is_superuser:
        # Basic Stats
        active_organizations = Organizations.objects.filter(is_active=True).count()
        inactive_organizations = Organizations.objects.filter(is_active=False).count()
        user_count = UserProfile.objects.filter(is_active=True).count()

        # Type-based Organization Count for Chart
        org_by_type = Organizations.objects.values('education_type').annotate(count=Count('id'))

        # Most Equipped Organizations
        most_equipped_orgs = (
            Organizations.objects.annotate(equipment_count=Count('org_room__roomsequipment'))
            .order_by('-equipment_count')[:5]
        )

        # Recent Equipment
        recent_equipments = RoomsEquipment.objects.order_by('-created')[:10]

        # Organizations by Region
        org_by_region = (
            Regions.objects.annotate(org_count=Count('organizations'))
            .order_by('-org_count')
        )
        

        # Retrieve historical records with old and new values for each change
        historical_records = []
        history_queryset = Organizations.history.order_by('-history_date')[:5]

        three_days_ago = timezone.now() - timedelta(days=3)
        last_equipments = RoomsEquipment.objects.filter(created__gte=three_days_ago)[:10]

        for record in history_queryset:
            changed_fields = []
            old_value, new_value = None, None
            if record.prev_record:
                diff = record.prev_record.diff_against(record)
                changed_fields = diff.changed_fields
                old_value = {field: diff.old_record.__dict__.get(field) for field in changed_fields}
                new_value = {field: record.__dict__.get(field) for field in changed_fields}

            historical_records.append({
                'instance': record.instance,
                'history_date': record.history_date,
                'history_change_reason': record.history_change_reason,
                'changed_fields': changed_fields,
                'old_value': old_value,
                'new_value': new_value,
            })

        context = {
            'active_organizations': active_organizations,
            'inactive_organizations': inactive_organizations,
            'user_count': user_count,
            'org_by_type': org_by_type,
            'most_equipped_orgs': most_equipped_orgs,
            'recent_equipments': recent_equipments,
            'org_by_region': org_by_region,
            'historical_records': historical_records,
            'last_equipments': last_equipments
        }

        return render(request, 'index.html', context)
    else:
        return redirect('home')

def schools(request):
    return render(request, 'schools/school-ratings.html')


def users(request):

    users = UserProfile.objects.filter(is_active=True, is_super_admin=False)

    context = {
        'users': users
    }

    return render(request, 'users/users-list.html', context)

@login_required
def organizations(request):
    org = Organizations.objects.filter(is_active=True)

    region_id = request.GET.get('region')
    district_id = request.GET.get('district')
    is_inclusive = request.GET.get('is_inclusive')
    rating = request.GET.get('rating')

    if region_id:
        org = org.filter(region_id=region_id)

    if district_id:
        org = org.filter(district_id=district_id)

    if is_inclusive is not None:
        org = org.filter(is_inclusive=is_inclusive == 'True')

    if rating:
        org = org.filter(rating=rating)

    regions = Regions.objects.all()
    districts = Districts.objects.all()

    context = {
        'organizations': org,
        'regions': regions,
        'districts': districts
    }

    return render(request, 'organizations/list.html', context)

@login_required
def organization_detail(request, org_id):

    organization = get_object_or_404(Organizations, id=org_id)
    
    if organization.is_active:
        context = {
            'organization': organization
        }
        
        return render(request, 'organizations/detail.html', context)
    else:
        return HttpResponse("<h1>Ushbu muassasa admin tomonidan o'chirilgan bo'lishi mumkin</h1>")


@login_required
def detail_profile(request, id):

    user = get_object_or_404(UserProfile, id=id)

    context = {
        'user': user
    }

    return render(request, 'users/user-profile-detail.html', context)


@login_required
def update_profile(request, id):

    user_data = get_object_or_404(UserProfile, id=id)

    if request.method == 'POST' and request.user.is_superuser:
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user_data)
        if form.is_valid():
            print("Topshirildi")
            form.save()
            return redirect('detail_profile', id)
        else:
            return HttpResponse(form.errors)
    else:
        form = UpdateProfileForm(instance=user_data)

    context = {
        'user_data': user_data,
        'form': form
    }

    return render(request, 'users/update-user-profile.html', context)


@login_required
def search_users(request):
    input_data = request.GET.get('searched_for')
    users = UserProfile.objects.filter(
        Q(first_name__icontains=input_data) | Q(last_name__icontains=input_data) | Q(tel_number__icontains = input_data)
    )

    context = {
        'users': users
    }

    return render(request, 'users/searched_user.html', context)


@login_required
def update_organization(request, org_id):
    organization = get_object_or_404(Organizations, id=org_id)

    if request.method == 'POST':
        form = UpdateOrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization_detail', org_id=organization.id)
    else:
        form = UpdateOrganizationForm(instance=organization)

    context = {
        'form': form,
        'organization': organization
    }

    return render(request, 'organizations/update.html', context)


@login_required
def create_organization(request):
    if request.method == 'POST':
        form = CreateOrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('organizations')
        else:
            print(form.errors)
    else:
        form = CreateOrganizationForm()

    context = {
        'form': form
    }
    return render(request, 'organizations/create.html', context)


@login_required
def delete_organization(request, org_id):
    if request.user.is_superuser and request.method=='POST':
        org = get_object_or_404(Organizations, id=org_id)
        org.is_active = False
        org.save()
        return redirect('organizations')
    else:
        return HttpResponse("Sizga mumkin emas")