from django.shortcuts import render, get_object_or_404, redirect

from .forms import UserRegisterForm, UserLoginForm, UserEditForm, ProfileEditForm

from django.contrib import messages
from django.contrib.auth import login, logout
from .models import Profile


def register(requset):
    if requset.method == 'POST':
        form = UserRegisterForm(requset.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(requset, user)
            messages.success(requset, 'Вы успешно зарегестрировались')
            return redirect('edit_cabinet')
        else:
            messages.error(requset, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(requset, 'registration/register.html', {'form': form})


def user_login(requset):
    if requset.method == 'POST':
        form = UserLoginForm(data=requset.POST)
        if form.is_valid():
            user = form.get_user()
            login(requset, user)
            return redirect('edit_cabinet')
    else:
        form = UserLoginForm()
    return render(requset, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def edit(request):
    profile = Profile.objects.get(user=request.user)
    print(profile)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_cabinet')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'registration/cabinet.html', {'user_form': user_form,
                                                             'profile_form': profile_form,
                                                             'profile': profile})
