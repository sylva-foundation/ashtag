from django.test.testcases import TestCase
from ashtag.apps.core.models import Survey, Sighting, Tree
from ashtag.apps.export.datacollections import SurveyCollection


class BaseCollectionTestCase(TestCase):

    def tree(self):
        return Tree.objects.create(
            creator_email='a@a.com',
            tag_number='12345',
            location='POINT(-51 1)',
        )

    def sighting(self, tree=None):
        tree = tree or self.tree()
        return Sighting.objects.create(
            creator_email=tree.creator_email,
            tree=tree,
            disease_state=True,
            location='POINT(-51 1)',
        )

    def survey(self, sighting=None, tree=None):
        return Survey.objects.create(
            sighting=sighting or self.sighting(tree),
            symptoms=[s[0] for s in Survey.SYMPTOMS[:2]],
            tree_size=Survey.TREE_SIZES[0][0],
            environment=Survey.ENVIRONMENTS[0][0],
            num_nearby_trees=Survey.NUM_NEARBY_TREES[1][0],
            nearby_disease_state=Survey.NEARBY_DISEASE_STATE[0][0],
        )

class SurveyCollectionTestCase(BaseCollectionTestCase):

    def setUp(self):
        self.collection = SurveyCollection()

    def test_get_queryset(self):
        survey = self.survey()

        records = [r for r in self.collection]
        self.assertEqual(len(records), 1)