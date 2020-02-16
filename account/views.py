from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import JsonResponse
from .models import Contact

def login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			login_form_cd = login_form.cleaned_data
			user = authenticate(request, username=login_form_cd['username'], password=login_form_cd['password'])

			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Login successfully!')
				else: return HttpResponse('Login failed!')
			else: return HttpResponse('Login failed!')
		else: return HttpResponse('Login failed!')
	else:
		login_form = LoginForm()
		return render(request, 'account/login.html', {'login_form':login_form})

def user_registration(request):
	if request.method == "POST":
		user_registration_form = UserRegistrationForm(request.POST)
		if user_registration_form.is_valid():
			new_user = user_registration_form.save(commit=False)
			new_user.set_password(user_registration_form.cleaned_data['first_password'])
			new_user.save()

			Profile.objects.create(user=new_user)
			return render(request, 'account/user_registration_done.html', {'new_user':new_user})
	else:
		user_registration_form = UserRegistrationForm()
		return render(request, 'account/user_registration.html', {'user_registration_form':user_registration_form})

@login_required
def user_edit(request):
	if request.method == 'POST':
		user_edit_form = UserEditForm(instance=request.user, data=request.POST)
		profile_edit_form = ProfileEditForm(instance=request.user.profile,
											data=request.POST,
											files=request.FILES)
		if user_edit_form.is_valid() and profile_edit_form.is_valid():
			user_edit_form.save()
			profile_edit_form.save()
			return HttpResponse('Edit successfully!')
		return HttpResponse('Edit failed!')
	else:
		user_edit_form = UserEditForm(instance=request.user)
		profile_edit_form = ProfileEditForm(instance=request.user.profile)

		return render(request, 'account/user_edit.html', {'user_edit_form':user_edit_form,
															'profile_edit_form':profile_edit_form})

@login_required
def feed(request):
	return render(request, 'account/feed.html', {'section':'feed'})

@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	return render(request, 'account/user_detail.html', {'user':user})

def user_list(request):
	users = User.objects.filter(is_active=True)
	return render(request, 'account/user_list.html', {'users':users})


@ajax_required
@require_POST
@login_required
def user_follow(request):
	user_id = request.POST.get('id')
	user_action = request.POST.get('action')

	if user_id and user_action:
		try:
			user_to = User.objects.get(id=user_id)
			if user_action == 'follow':
				Contact.user_from.get_or_create(user_from=request.user, user_to=user_to)
			else:
				Contact.user_from.filter(user_from=request.user, user_to=user_to).delete()
		except:
			pass
	return JsonResponse({'status': 200})
