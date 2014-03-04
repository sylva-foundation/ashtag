from hashlib import sha1
from datetime import datetime, timedelta

from django.db.models import Q
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.core.mail import EmailMessage

from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils import Choices
from multiselectfield.db.fields import MultiSelectField

from .utils import pk_generator


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
    display_sighting = models.OneToOneField('Sighting', null=True, default=None, on_delete=models.SET_NULL, related_name='displayed_on_set')
    creator_email = models.EmailField(max_length=254)

    tag_checked_by = models.ForeignKey(User, blank=True, null=True)
    tag_number = models.CharField(
        max_length=10, db_index=True, null=True, blank=True)
    location = models.PointField()

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

    def save(self, *args, **kwargs):
        self.update_display_sighting()
        super(Tree, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sightings:tree', args=[self.tag_or_id])

    def update_display_sighting(self):
        self.display_sighting = self.find_display_sighting()

    def find_display_sighting(self):
        """Get the sighting which should be displayed for this tree

        We assume this should be the lastest sighting by the tree's creator

        NOTE: You should normally use the display_sighting field as it
              will be more performant
        """
        qs = self.sighting_set.filter(
            creator_email=self.creator_email,
            hidden=False,
        )
        try:
            sighting = qs.latest()
        except Sighting.DoesNotExist:
            sighting = None
        return sighting

    @property
    def disease_state(self):
        # For now we just take the disease_state of the current display_sighting
        return self.display_sighting.disease_state

    @property
    def tag_or_id(self):
        return self.tag_number or self.pk


class Sighting(CreatorMixin, models.Model):
    """Sighting, recording date, time, location, notes, image, tree, state."""
    DISEASE_STATE = Choices(
        (None, 'unknown', "Uncertain"),
        (True, 'diseased', "Likely"),
        (False, 'notdiseased', "Unlikely"),
    )

    id = models.CharField(max_length=6, primary_key=True, default=pk_generator)
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')
    creator_email = models.EmailField(max_length=254)
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE, related_name='sightings')
    image = models.ImageField(upload_to=lambda i, fn: 'sightings/%s/%s-%s' % (i.id, pk_generator(10), fn))
    image_hash = models.CharField(max_length=50, default='', blank=True)
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

    def save(self, *args, **kwargs):
        super(Sighting, self).save(*args, **kwargs)
        tree = self.tree
        tree.update_display_sighting()
        tree.save()

    def __unicode__(self):
        return u"{0} @ {1}".format(self.tree, self.created)

    def get_absolute_url(self):
        if self.tree.tag_number:
            return reverse('sightings:tree', args=[self.tree.tag_number])
        else:
            return reverse('sightings:map')

    def set_image_hash(self, f):
        f.seek(0)
        img_hash = sha1(f.read())
        f.seek(0)
        self.image_hash = img_hash.hexdigest()

    def is_duplicate(self):
        time_threshold = datetime.now() - timedelta(hours=12)
        try:
            duplicate = Sighting.objects.filter(
                creator_email=self.creator_email,
                image_hash=self.image_hash,
                location=self.location,
                notes=self.notes,
                created__gt=time_threshold,
            ).exclude(pk=self.pk).latest()
        except Sighting.DoesNotExist:
            return None

        return duplicate


class Comment(models.Model):
    """A comment, can be used on a sighting."""
    created = AutoCreatedField('created')
    modified = AutoLastModifiedField('modified')
    creator_email = models.EmailField(max_length=254)

    comment = models.TextField()
    tree = models.ForeignKey('Tree', on_delete=models.CASCADE)

    class Meta:
        abstract = True  # Just testing for now


class Survey(CreatorMixin, models.Model):
    """For storing Living Ash Project survey data"""

    SYMPTOMS = (
        ('dead top and shoots', 'Dead top and shoots'),
        ('dead bark and shoots', 'Dead bark and shoots'),
        ('dead bark on stem', 'Dead bark on stem'),
        ('dead bark at stem base', 'Dead bark at stem base'),
    )
    TREE_SIZES = (
        ('less than 5cm', 'Less than 5cm'),
        ('5-15cm', '5-15cm'),
        ('15-30cm', '15-30cm'),
        ('greater than 30cm', 'Greater than 30cm'),
    )
    ENVIRONMENTS = (
        ('forest or wood', 'Forest or wood'),
        ('park', 'Park'),
        ('hedgerow', 'Hedgerow'),
        ('garden', 'Garden'),
        ('street', 'Street'),
        ('nursery', 'Nursery'),
        ('new plantation', 'New plantation'),
    )
    NUM_NEARBY_TREES = (
        ('0', 'No'),
        ('1-2', '1-2'),
        ('3-5', '3-5'),
        ('6-10', '6-10'),
        ('11-20', '11-20'),
        ('more than 20', 'More than 20'),
    )
    NEARBY_DISEASE_STATE = (
        ('unknown', 'Uncertain'),
        ('diseased', 'Likely'),
        ('notdiseased', 'Unlikely'),
    )
    
    id = models.CharField(max_length=6, primary_key=True, default=pk_generator)
    created = AutoCreatedField('created')
    sighting = models.OneToOneField('Sighting', on_delete=models.CASCADE, related_name='surveys')

    symptoms = MultiSelectField(choices=SYMPTOMS, default='', blank=True)
    tree_size = models.CharField(max_length=30, choices=TREE_SIZES, default='', blank=True)
    environment = models.CharField(max_length=30, choices=ENVIRONMENTS, default='', blank=True)
    num_nearby_trees = models.CharField(max_length=30, choices=NUM_NEARBY_TREES, default='', blank=True)
    nearby_disease_state = models.CharField(max_length=30, choices=NEARBY_DISEASE_STATE, default='', blank=True)

    def enforce_choices(self):
        allowed_symptoms = [x[0] for x in Survey.SYMPTOMS]
        self.symptoms = filter(lambda s: s in allowed_symptoms, self.symptoms)

        if self.tree_size not in [x[0] for x in Survey.TREE_SIZES]:
            self.tree_size = ''

        if self.environment not in [x[0] for x in Survey.ENVIRONMENTS]:
            self.environment = ''

        if self.num_nearby_trees not in [x[0] for x in Survey.NUM_NEARBY_TREES]:
            self.num_nearby_trees = ''

        if self.nearby_disease_state not in [x[0] for x in Survey.NEARBY_DISEASE_STATE]:
            self.nearby_disease_state = ''



class EmailTemplate(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    description = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    enabled = models.BooleanField(default=True, help_text='Should this email actually be sent?')
    default_to = models.TextField(default='', blank=True, help_text='Who should this email be sent to by default? Only applies to admin-related emails. Separate multiple emails using commas.')

    @staticmethod
    def send(template_name, to_emails=None, **kwargs):
        obj = EmailTemplate.objects.get(name=template_name)
        obj.send_delayed(to_emails, **kwargs)

    def parse_default_to(self):
        default_to = self.default_to or ''
        emails = default_to.split(',')
        emails = [e.strip() for e in emails if e.strip()]
        return emails

    def make_email(self, to_emails=None, **kwargs):
        to_emails = to_emails or self.parse_default_to()
        body_template = Template(self.body)
        subject_template = Template(self.subject)
        context = kwargs

        if hasattr(self, "context_%s" % self.name):
            method = getattr(self, "context_%s" % self.name)
            extra_context = method(**kwargs)
            if extra_context:
                context.update(extra_context)

        body = body_template.render(Context(context))
        subject = subject_template.render(Context(context))

        email = EmailMessage(subject, body, to=to_emails)
        return email

    def send_delayed(self, to_emails=None, **kwargs):
        from .tasks import send_email
        if not self.enabled:
            return
        email = self.make_email(to_emails=to_emails, **kwargs)
        send_email.delay(email)

    def context_new_untagged_tree(self, request, **kwargs):
        return {
            'buy_tags_url': request.build_absolute_uri(reverse('store:tagpacks')),
        }

    def context_new_sighting_to_owner(self, request, sighting, **kwargs):
        tree = sighting.tree
        return {
            'url': request.build_absolute_uri(sighting.get_absolute_url()),
            'sighting': sighting,
            'tree': tree,
            'user': tree.creator,
        }

    def context_admin_new_tag(self, request, tree, this_tree_was, **kwargs):
        return {
            'url': request.build_absolute_uri(tree.get_absolute_url()),
            'admin_url': request.build_absolute_uri(reverse('admin:core_tree_changelist')),
            'this_tree_was': this_tree_was,
        }

    def context_admin_flagged(self, request, obj, **kwargs):
        if isinstance(obj, Tree):
            url_name = 'admin:core_tree_change'
            the_item = 'a tree'
        else:
            url_name = 'admin:core_sighting_change'
            the_item = 'a sighting'

        return {
            'url': request.build_absolute_uri(obj.get_absolute_url()),
            'admin_url': request.build_absolute_uri(reverse(url_name, args=[obj.id])),
            'email': request.user.email if request.user.is_authenticated() else 'anonymous',
            'the_item': the_item,
        }








