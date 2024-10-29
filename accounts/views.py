from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import SignInForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from school.models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                error_message = "Foydalanuvchi nomi yoki parol xato !"

                context = {
                    'form': form,
                    'error_message': error_message
                }

                return render(request, 'auth/login.html', context)
    else:
        form = SignInForm()


    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            create_new_user = User.objects.create_user(
                username=form_data['passport_id'],
                password=form_data['password']
            )

            new_user_profile = form.save(commit=False)
            new_user_profile.user = create_new_user
            new_user_profile.save()

            return redirect('detail_profile', new_user_profile.id)
        else:
            return HttpResponse(form.errors)

    return render(request, 'users/add-user.html')


@login_required
def delete_user(request, passport_id):
    if request.user.is_staff:
        get_user = get_object_or_404(UserProfile, passport_id=passport_id)
        get_user.delete()
        return redirect('users')