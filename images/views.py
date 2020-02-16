from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from .forms import AddImageForm
from .models import Image
from common.decorators import ajax_required

@login_required
def add_image(request):
	if request.method == 'POST':
		form = AddImageForm(data = request.POST)
		if form.is_valid():
			image = form.save(commit=False)
			image.user = request.user
			image.save()

			messages.success(request, 'Image has been successfully0 added!')
			return redirect(image.get_absolute_url())
	else:
		form = AddImageForm(data = request.GET)
		return render(request, 'images/add_image.html', {'form':form, 'section':'images'})

def detail_image(request, id, slug):
	image = get_object_or_404(Image, id=id, slug=slug)
	return render(request, 'images/detail_image.html', {'image':image, 'section':'image'})

@ajax_required
@login_required
@require_POST
def like_image(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_liked.add(request.user)
			elif action == 'dislike':
				image.users_liked.remove(request.user)
				return JsonResponse({'status':200})
		except:
			pass
	return JsonResponse({'status':200})

@login_required
def list_liked_images(request):
	images = Image.objects.filter(users_liked=request.user)
	images_paginator = Paginator(images, 8)
	page = request.GET.get('page')
	try:
		images = images_paginator.page(page)
	except PageNotAnInteger:
		images = images_paginator.page(1)
		page = 1
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		images = images_paginator.page(images_paginator.num_pages)
		page = images_paginator.num_pages
	if request.is_ajax():
		return render(request, 'images/list_liked_images_ajax.html', {'images':images, 'page':page})
	return render(request, 'images/list_liked_images.html', {'section':'images', 'images':images, 'page':page})

def all_images(request):
	images = Image.objects.all()
	return render(request, 'images/all_images.html', {'images':images})