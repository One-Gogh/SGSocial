from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'images_created')
	users_liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
	image = models.ImageField(upload_to = 'images/%Y/%m/%d')
	title= models.CharField(max_length=200)
	description = models.TextField(blank=True)
	slug = models.SlugField(max_length = 200, blank=True)
	url = models.URLField()
	date = models.DateField(auto_now_add=True, db_index=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Image, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('images:detail_image', args=[self.id, self.slug])