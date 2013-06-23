from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils import Choices

from ashtag.apps.core.utils import pk_generator


class CreatorMixin(object):
    """Mixin providing the email details of the creator (User or email)."""

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


class Tree(CreatorMixin, models.Model):
    """A tree, complete with tag number."""
    id = models.CharField(max_length=6, primary_key=True, default=pk_generator)
    created = AutoCreatedField('created')
    creator_email = models.EmailField(max_length=254)

    tag_checked_by = models.ForeignKey(User, blank=True, null=True)
    tag_number = models.CharField(
        max_length=10, db_index=True, null=True, blank=True)
    location = models.PointField()

    exemplar = models.ForeignKey(
        'Sighting',
        blank=True, null=True,
        related_name='exemplary_of',
        help_text="Which sighting is to be shown on the tree page big image?")

    flagged = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    objects = models.GeoManager()

    class Meta:
        ordering = ('-created',)
        get_latest_by = ('created',)

    def __unicode__(self):
        if self.tag_number:
            return u"Claimed Tree #{0}".format(self.tag_number)
        else:
            return u"Unclaimed Tree {0}".format(self.id)

    def get_absolute_url(self):
        return reverse('sightings:tree', args=[self.tag_number or self.pk])

    @property
    def display_sighting(self):
        """Get the sighting which should be displayed for this tree

        We assume this should be the lastest sighting by the tree's creator
        """
        qs = self.sighting_set.filter(
            creator_email=self.creator_email,
            hidden=False
        )
        return qs.latest()


class Sighting(CreatorMixin, models.Model):
    """Sighting, recording date, time, location, notes, image, tree, state."""
    DISEASE_STATE = Choices(
        (None, 'unknown', "I don't know"),
        (True, 'diseased', "Diseased"),
        (False, 'notdiseased', "Not diseased"),
    )

    id = models.CharField(max_length=6, primary_key=True, default=pk_generator)
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')
    creator_email = models.EmailField(max_length=254)
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sightings/%Y/%m/%d')
    disease_state = models.NullBooleanField(
        choices=DISEASE_STATE, default=DISEASE_STATE.unknown)
    location = models.PointField()
    notes = models.TextField(blank=True, null=True)

    flagged = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

    objects = models.GeoManager()

    class Meta:
        ordering = ('-created',)
        get_latest_by = ('created',)

    def __unicode__(self):
        return u"{0} @ {1}".format(self.tree, self.created)

    def get_absolute_url(self):
        if self.tree.tag_number:
            return reverse('sightings:tree', args=[self.tree.tag_number])
        else:
            return reverse('sightings:map')


class Comment(models.Model):
    """A comment, can be used on a sighting."""
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')
    creator_email = models.EmailField(max_length=254)

    comment = models.TextField()
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)

    class Meta:
        abstract = True  # Just testing for now
