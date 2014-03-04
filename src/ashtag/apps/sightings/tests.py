#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from django_webtest import WebTest

from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core import mail
from ashtag.apps.core.models import Survey

from ..core.models import Sighting, Tree

X_IMAGE = """data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wgARCAABAAEDAREAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACP/EABQBAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhADEAAAAVSf/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABBQJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPwF//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPwF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQAGPwJ//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPyF//9oADAMBAAIAAwAAABCf/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPxB//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPxB//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxB//9k="""


class SightingTestCase(WebTest):
    """Test that a tree tagger and spotter can do certain things."""
    csrf_checks = False
    fixtures = ["email-templates"]

    @classmethod
    def setUpClass(cls):
        cls.tagger = User.objects.create(
            email='a@b.com',
            username='ab',
            password='123',
        )
        cls.tagged_tree = Tree.objects.create(
            creator_email='a@b.com',
            location="POINT (0 0)",
            tag_number=1234,
        )
        cls.anon_tree = Tree.objects.create(
            creator_email='c@d.com',
            location="POINT (0 0)",
        )
        cls.good_sighting = Sighting.objects.create(
            tree=cls.tagged_tree,
            creator_email='c@d.com',
            location="POINT (0 0)",
            notes="Test Good Sighting")
        cls.bad_sighting = Sighting.objects.create(
            tree=cls.tagged_tree,
            creator_email='evil@nasty.com',
            location="POINT (0 0)",
            notes="Teh Pr0nz!!!!111oneone")

    def tearDown(self):
        self.tagged_tree.sighting_set.update(
            flagged=False, hidden=False)
        Tree.objects.update(hidden=False, flagged=False)

    def _get_thing(self, thing):
        """Get a fresh copy of the thing from the DB."""
        return thing.__class__.objects.get(id=thing.id)

    def test_get_creator(self):
        """Check that the creator attribute resolves to a user if present."""
        self.assertEqual(self.tagger, self.tagged_tree.creator)
        self.assertEqual(None, self.anon_tree.creator)

    def test_creator_flagging_hides_update(self):
        """If a creator flags an update, it should hide immediately."""
        response = self.app.get(reverse('sightings:tree', args=[1234]))
        self.assertContains(response, str(self.bad_sighting.notes))

        response = self.app.post(
            reverse('sightings:flag', args=[1234]),
            {'sighting': self.bad_sighting.id},
            user=self.tagger)
        self.assertContains(response, 'remove')
        self.assertEqual(True, self._get_thing(self.bad_sighting).hidden)
        self.assertEqual(True, self._get_thing(self.bad_sighting).flagged)

        response = self.app.get(reverse('sightings:tree', args=[1234]))
        self.assertNotContains(response, self.bad_sighting.notes)

    def test_spotter_flagging_flags_update(self):
        """If a spotter flags an update, it should flag but not hide."""
        response = self.app.get(reverse('sightings:tree', args=[1234]))
        self.assertContains(response, str(self.bad_sighting.notes))

        response = self.app.post(
            reverse('sightings:flag', args=[1234]),
            {'sighting': self.bad_sighting.id})
        self.assertContains(response, 'flag')
        self.assertEqual(False, self._get_thing(self.bad_sighting).hidden)
        self.assertEqual(True, self._get_thing(self.bad_sighting).flagged)

        self.assertEqual(1, len(mail.outbox))

        response = self.app.get(reverse('sightings:tree', args=[1234]))
        self.assertContains(response, self.bad_sighting.notes)
        self.assertContains(response, 'class="flagged"')

    def test_anyone_flagging_tree(self):
        """If anyone flags a whole tree, then we should email the managers."""
        response = self.app.get(reverse('sightings:tree', args=[1234]))
        response = self.app.post(
            reverse('sightings:flag', args=[1234]),
            {'tree': self.tagged_tree})
        self.assertContains(response, 'flag')
        self.assertEqual(True, self._get_thing(self.tagged_tree).flagged)
        self.assertEqual(False, self._get_thing(self.tagged_tree).hidden)
        self.assertEqual(1, len(mail.outbox))

    @unittest.skip("Weird error about compressor... why?")
    def test_flagged_tree_inaccessible(self):
        """A flagged tree shouldn't be accesible."""
        self.tagged_tree.hidden = True
        self.tagged_tree.flagged = True
        self.tagged_tree.save()
        self.app.get(reverse('sightings:tree', args=[1234]), status=404)

    def test_offline_submission(self):
        """Check that offline-style submission still works (302, redirect)."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'tag_number': '12345',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test offline',
            }, user=self.tagger, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)

    def test_submit_anon(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',
            }, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        self.assertEqual(1, len(mail.outbox))

    def test_tagger_emailed_on_update(self):
        """Tagger should get an email when a tree is updated by a spotter."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '12345',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',
            }, status=302, user=self.tagger)
        self.assertEqual(1, len(mail.outbox))

class SightingSurveyTestCase(WebTest):
    """Test that a tree tagger and spotter can do certain things."""
    csrf_checks = False
    fixtures = ["email-templates"]

    def test_submit_survey_valid_choices(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',

                'survey_symptoms': 'dead top and shoots',
                'survey_tree_size': '5-15cm',
                'survey_environment': 'street',
                'survey_num_nearby_trees': '11-20',
                'survey_nearby_disease_state': 'diseased',
            }, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        sighting = Sighting.objects.get()
        surveys = Survey.objects.all()
        self.assertEqual(len(surveys), 1)
        survey = surveys[0]
        self.assertEqual(survey.make_sighting, sighting)
        self.assertEqual(survey.symptoms, ['dead top and shoots'])
        self.assertEqual(survey.tree_size, '5-15cm')
        self.assertEqual(survey.environment, 'street')
        self.assertEqual(survey.num_nearby_trees, '11-20')
        self.assertEqual(survey.nearby_disease_state, 'diseased')

    def test_submit_survey_no_values(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',

                'survey_symptoms': '',
                'survey_tree_size': '',
                'survey_environment': '',
                'survey_num_nearby_trees': '',
                'survey_nearby_disease_state': '',
            }, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        sighting = Sighting.objects.get()
        surveys = Survey.objects.all()
        self.assertEqual(len(surveys), 0)

    def test_submit_survey_no_valid_choices(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',

                'survey_symptoms': 'aaa',
                'survey_tree_size': 'bbb',
                'survey_environment': 'ccc',
                'survey_num_nearby_trees': 'ddd',
                'survey_nearby_disease_state': 'eee',
            }, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        sighting = Sighting.objects.get()
        surveys = Survey.objects.all()
        self.assertEqual(len(surveys), 0)

    def test_submit_survey_some_bad_choices(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            {
                'creator_email': 'test@example.com',
                'tag_number': '',
                'image': X_IMAGE,
                'image_name': 'xxx.jpg',
                'disease_state': 'True',
                'location': 'POINT (0 0)',
                'notes': 'test anon',

                'survey_symptoms': 'dead top and shoots',
                'survey_tree_size': 'xxx',
                'survey_environment': 'street',
                'survey_num_nearby_trees': 'yyy',
                'survey_nearby_disease_state': 'diseased',
            }, status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        sighting = Sighting.objects.get()
        surveys = Survey.objects.all()
        self.assertEqual(len(surveys), 1)
        survey = surveys[0]
        self.assertEqual(survey.make_sighting, sighting)
        self.assertEqual(survey.symptoms, ['dead top and shoots'])
        self.assertEqual(survey.tree_size, '')
        self.assertEqual(survey.environment, 'street')
        self.assertEqual(survey.num_nearby_trees, '')
        self.assertEqual(survey.nearby_disease_state, 'diseased')

    def test_submit_survey_multiple_symptoms(self):
        """User should be able to submit with email only."""
        response = self.app.post(
            reverse('sightings:submit'),
            (
                ('creator_email', 'test@example.com'),
                ('tag_number', ''),
                ('image', X_IMAGE),
                ('image_name', 'xxx.jpg'),
                ('disease_state', 'True'),
                ('location', 'POINT (0 0)'),
                ('notes', 'test anon'),

                ('survey_symptoms', 'dead top and shoots'),
                ('survey_symptoms', 'dead bark at stem base'),
                ('survey_tree_size', '5-15cm'),
                ('survey_environment', 'street'),
                ('survey_num_nearby_trees', '11-20'),
                ('survey_nearby_disease_state', 'diseased'),
            ), status=302)
        self.assertTrue(reverse('sightings:sent') in response.location)
        sighting = Sighting.objects.get()
        surveys = Survey.objects.all()
        self.assertEqual(len(surveys), 1)
        survey = surveys[0]
        self.assertEqual(survey.make_sighting, sighting)
        self.assertEqual(survey.symptoms, ['dead top and shoots', 'dead bark at stem base'])
        self.assertEqual(survey.tree_size, '5-15cm')
        self.assertEqual(survey.environment, 'street')
        self.assertEqual(survey.num_nearby_trees, '11-20')
        self.assertEqual(survey.nearby_disease_state, 'diseased')
