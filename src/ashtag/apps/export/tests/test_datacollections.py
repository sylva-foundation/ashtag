from ashtag.apps.export.datacollections import SurveyCollection, SightingCollection, UserCollection
from ashtag.apps.export.tests.base import BaseExportTestCase


class BaseCollectionTestCase(BaseExportTestCase):
    pass


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