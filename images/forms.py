from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class AddImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('url', 'title', 'description')
		widgets = {'url':forms.HiddenInput}
	
	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		url_extension = url.rsplit('.', 1)[1].lower()
		if url_extension not in valid_extensions:
			raise forms.ValidationError('Not valid image extension!')
		return url

	def save(self, force_insert=False, force_update=False, commit=True):
		image = super().save(commit=False)
		image_url = self.cleaned_data['url']
		response = request.urlopen(image_url)
		image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower)
		image.image.save(image_name, ContentFile(response.read()), save=False)
		if commit:
			image.save()
		return image