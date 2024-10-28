from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import OrganizationStatistics
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Organizations, Regions, Districts, Cities
from accounts.forms import UpdateProfileForm
from django.db.models import Q
from .forms import OrganizationUpdateForm, CreateOrganizationForm


@login_required
def dashboard(request):

    stats = OrganizationStatistics.objects.all()

    context = {
        'stats': stats
    }

    return render(request, 'index.html', context)


def schools(request):
    return render(request, 'schools/school-ratings.html')


def users(request):

    users = UserProfile.objects.all()

    context = {
        'users': users
    }

    return render(request, 'users/users-list.html', context)

@login_required
def organizations(request):
    org = Organizations.objects.all()

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
    
    context = {
        'organization': organization
    }
    
    return render(request, 'organizations/detail.html', context)


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
        form = UpdateProfileForm(request.POST, request.FILES, instance=user_data)
        if form.is_valid():
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
        Q(first_name__icontains=input_data) | Q(last_name__icontains=input_data)
    )

    context = {
        'users': users
    }

    return render(request, 'users/searched_user.html', context)


@login_required
def update_organization(request, org_id):
    organization = get_object_or_404(Organizations, id=org_id)

    if request.method == 'POST':
        form = OrganizationUpdateForm(request.POST, instance=organization)
        if form.is_valid():
            form.save()
            return redirect('organization_detail', org_id=organization.id)
    else:
        form = OrganizationUpdateForm(instance=organization)

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