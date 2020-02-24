import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Event


def create_event(user, verb, target=None):
	now = timezone.now()
	last_minute = now - datetime.timedelta(seconds=60)
	similar_events = Event.objects.filter(user_id=user.id, verb=verb,
										created__gte=last_minute)

	if target:
		target_type = ContentType.objects.get_for_model(target)
		similar_events = similar_events.filter(target_type=target_type,
											target_id=target.id)

	if not similar_events:
		event = Event(user=user, verb=verb, target=target)
		event.save()
		return True
	return False