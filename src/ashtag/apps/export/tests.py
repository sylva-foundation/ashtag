from datetime import datetime
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from pytz import UTC
from ashtag.apps.core.models import Survey, Sighting, Tree
from ashtag.apps.export.datacollections import SurveyCollection, SightingCollection, UserCollection


class BaseCollectionTestCase(TestCase):
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

class SurveyCollectionTestCase(BaseCollectionTestCase):
    collection_class = SurveyCollection

    def test_get_queryset(self):
        survey = self.collection.get_queryset().get()
        self.assertEqual(survey, self.survey)

    def test_iterator(self):
        records = [r for r in self.collection]
        self.assertEqual(len(records), 1)

    def test_prepare_record(self):
        record = self.collection.prepare_record(self.survey)

        self.assertEqual(record['id'], self.survey.pk)
        self.assertEqual(record['tree'], self.tree.pk)
        self.assertEqual(record['tag_number'], '12345')
        self.assertEqual(record['sighting'], self.sighting.pk)
        self.assertEqual(record['email'], 'a@a.com')
        self.assertEqual(record['user'], self.user.pk)
        self.assertEqual(record['date'], self.now_iso)
        self.assertEqual(record['repeat_url'], 'http://www.ashtag.org/sightings/submit/?tag_number=12345&survey=1')

        self.assertEqual(record['symptoms'], 'dead top and shoots, dead bark and shoots')
        self.assertEqual(record['tree_size'], 'less than 5cm')
        self.assertEqual(record['environment'], 'forest or wood')
        self.assertEqual(record['num_nearby_trees'], '1-2')
        self.assertEqual(record['nearby_disease_state'], 'unknown')

    def test_fields_match(self):
        record = self.collection.prepare_record(self.survey)
        self.assertSetEqual(set(record.keys()), set(self.collection.fields))


class SightingCollectionTestCase(BaseCollectionTestCase):
    collection_class = SightingCollection

    def test_get_queryset(self):
        sighting = self.collection.get_queryset().get()
        self.assertEqual(sighting, self.sighting)

    def test_iterator(self):
        records = [r for r in self.collection]
        self.assertEqual(len(records), 1)

    def test_prepare_record(self):
        record = self.collection.prepare_record(self.sighting)

        self.assertEqual(record['id'], self.sighting.pk)
        self.assertEqual(record['tree'], self.tree.pk)
        self.assertEqual(record['tag_number'], '12345')
        self.assertEqual(record['date'], self.now_iso)
        self.assertIn('foo/bar.png', record['image'])
        self.assertEqual(record['disease_state'], 'Likely')
        self.assertEqual(record['longitude'], 1.0)
        self.assertEqual(record['latitude'], -51.0)
        self.assertEqual(record['notes'], 'Some notes')

    def test_fields_match(self):
        record = self.collection.prepare_record(self.sighting)
        self.assertSetEqual(set(record.keys()), set(self.collection.fields))


class UserCollectionTestCase(BaseCollectionTestCase):
    collection_class = UserCollection

    def test_get_queryset(self):
        user = self.collection.get_queryset().get()
        self.assertEqual(user, self.user)

    def test_iterator(self):
        records = [r for r in self.collection]
        self.assertEqual(len(records), 1)

    def test_prepare_record(self):
        record = self.collection.prepare_record(self.user)

        self.assertEqual(record['id'], self.user.pk)
        self.assertEqual(record['username'], 'testuser')
        self.assertEqual(record['email'], 'a@a.com')
        self.assertEqual(record['date_joined'], self.now_iso)

    def test_fields_match(self):
        record = self.collection.prepare_record(self.user)
        self.assertSetEqual(set(record.keys()), set(self.collection.fields))
