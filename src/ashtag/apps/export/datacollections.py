from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ashtag.apps.core.models import Survey, Sighting


class BaseCollection(object):
    fields = None

    def __init__(self):
        self.queryset_iterator = self.get_queryset().iterator()

    def __iter__(self):
        return self

    def next(self):
        return self.prepare_record(self.queryset_iterator.next())

    def get_queryset(self):
        """ Return a queryset from which the collection will be formed

        :rtype: django.db.models.query.QuerySet
        """
        raise NotImplemented()

    def prepare_record(self, inst):
        """
        Prepare an individual model instance as given by get_queryset()

        :param inst: django.contrib.gis.db.models.Model
        :return: dict
        """
        raise NotImplemented()


class SurveyCollection(BaseCollection):
    fields = [
            # Standard fields
            'id', 'tree', 'tag_number', 'sighting', 'email', 'user', 'date', 'repeat_url',
            # Answer fields
            'symptoms', 'tree_size', 'environment', 'num_nearby_trees', 'nearby_disease_state',
        ]

    def get_queryset(self):
        return Survey.objects.filter(sighting__hidden=False, sighting__tree__hidden=False)

    def make_repeat_url(self, tree):
        if not tree.tag_number:
            # We can only have repeat URLs for tagged trees
            return None

        url = reverse('sightings:submit')
        url = 'http://www.ashtag.org%s?tag_number=%s&survey=1' % (url, tree.tag_number)
        return url

    def prepare_record(self, survey):
        sighting = survey.sighting
        tree = sighting.tree
        creator = survey.sighting.creator
        return dict(
            id=survey.pk,
            tree=tree.pk,
            tag_number=tree.tag_number,
            sighting=sighting.pk,
            email=sighting.creator_email,
            user=creator.pk if creator else None,
            date=survey.created.isoformat(),
            repeat_url=self.make_repeat_url(tree),

            symptoms=', '.join(survey.symptoms),
            tree_size=survey.tree_size,
            environment=survey.environment,
            num_nearby_trees=survey.num_nearby_trees,
            nearby_disease_state=survey.nearby_disease_state,
        )


class SightingCollection(BaseCollection):
    """ Provides anonymous sighting data """
    fields = [
        'id', 'tree', 'tag_number', 'date', 'image', 'disease_state', 'latitude', 'longitude', 'notes',
    ]

    def get_queryset(self):
        return Sighting.objects.filter(hidden=False, tree__hidden=False)

    def prepare_record(self, sighting):
        tree = sighting.tree

        return dict(
            id=sighting.pk,
            tree=tree.pk,
            tag_number=tree.tag_number,
            date=sighting.created.isoformat(),
            image=sighting.image.url if sighting.image else None,
            disease_state=sighting.get_disease_state_display(),
            latitude=sighting.location.y,
            longitude=sighting.location.x,
            notes=sighting.notes,
        )

class UserCollection(BaseCollection):
    fields = [
        'id', 'username', 'email', 'date_joined'
    ]

    def get_queryset(self):
        return User.objects.all()

    def prepare_record(self, user):
        return dict(
            id=user.pk,
            username=user.username,
            email=user.email,
            date_joined=user.date_joined.isoformat(),
        )

