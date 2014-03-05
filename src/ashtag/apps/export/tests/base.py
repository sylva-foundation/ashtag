from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase
from pytz import UTC
from ashtag.apps.core.models import Tree, Sighting, Survey


class BaseExportTestCase(TestCase):
    collection_class = None

    def setUp(self):
        self.now = datetime(year=2012, month=3, day=4, hour=12, minute=30, second=10, tzinfo=UTC)
        self.now_iso = '2012-03-04T12:30:10+00:00'

        self.tree = self.make_tree()
        self.sighting = self.make_sighting(self.tree)
        self.survey = self.make_survey(sighting=self.sighting)
        self.user = self.make_user()
        self.collection = self.collection_class()

    def make_tree(self):
        return Tree.objects.create(
            creator_email='a@a.com',
            tag_number='12345',
            location='POINT(1 -51)',
            created=self.now,
        )

    def make_sighting(self, tree=None):
        tree = tree or self.make_tree()
        return Sighting.objects.create(
            creator_email=tree.creator_email,
            tree=tree,
            disease_state=True,
            location='POINT(1 -51)',
            created=self.now,
            image='/foo/bar.png',
            notes='Some notes',
        )

    def make_survey(self, sighting=None, tree=None):
        return Survey.objects.create(
            sighting=sighting or self.make_sighting(tree),
            symptoms=[s[0] for s in Survey.SYMPTOMS[:2]],
            tree_size=Survey.TREE_SIZES[0][0],
            environment=Survey.ENVIRONMENTS[0][0],
            num_nearby_trees=Survey.NUM_NEARBY_TREES[1][0],
            nearby_disease_state=Survey.NEARBY_DISEASE_STATE[0][0],
            created=self.now,
        )

    def make_user(self):
        return User.objects.create(
            username='testuser',
            email='a@a.com',
            date_joined=self.now,
        )
