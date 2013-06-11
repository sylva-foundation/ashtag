from django.contrib.gis.db import models
from django.contrib.auth.models import User

from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils import Choices

from ashtag.apps.core.utils import pk_generator


class RandomIdMixin(object):
    id = models.CharField(max_length=6, primary_key=True, default=pk_generator)

class TimestampedMixin(object):
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')

class CreatorMixin(object):
    creator_email = models.EmailField()

    @property
    def creator(self):
        if hasattr(self, '_creator'):
            return self._creator

        if not self.creator_email:
            self._creator = None

        try:
            self._creator = User.objects.get(email=self.creator_email)
        except User.DoesNotExist:
            self._creator = None
        
        return self._creator


class Tree(RandomIdMixin, TimestampedMixin, CreatorMixin, models.Model):
    tag_number = models.CharField(max_length=10, db_index=True, null=True, blank=True)


    class Meta:
        abstract = True # Just testing for now

class Sighting(RandomIdMixin, TimestampedMixin, CreatorMixin, models.Model):
    DISEASE_STATE = Choices(
        (None, 'unknown', "I don't know"),
        (True, 'diseased', "Diseased"),
        (False, 'notdiseased', "Not diseased"),
    )

    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sightings/%Y/%m/%d')
    disease_state = models.NullBooleanField(choices=DISEASE_STATE, default=DISEASE_STATE.unknown)
    location = models.PointField()
    notes = models.TextField(blank=True, null=True)

    objects = models.GeoManager()


    class Meta:
        abstract = True # Just testing for now

class Comment(TimestampedMixin, CreatorMixin, models.Model):
    comment = models.TextField()
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)

    class Meta:
        abstract = True # Just testing for now