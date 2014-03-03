#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from decimal import Decimal

from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.mail import mail_managers

from ashtag.apps.core.models import Sighting, Tree, EmailTemplate


class SightingForm(forms.ModelForm):
    tag_number = forms.CharField(max_length=5, required=False)

    class Meta:
        model = Sighting
        exclude = ('id', 'tree', 'created', 'modified', 'creator_email')

    def __init__(self, request, user, *args, **kwargs):
        super(SightingForm, self).__init__(*args, **kwargs)
        self.request = request
        self.user = user

    def save(self, *args, **kwargs):
        sighting = super(SightingForm, self).save(*args, **kwargs)
        sighting.set_image_hash(self.cleaned_data['image'])
        return sighting

    def clean_tag_number(self):
        tag_number = self.cleaned_data['tag_number']
        if not tag_number:
            return tag_number
        try:
            int(tag_number)
        except ValueError:
            raise forms.ValidationError('Tag number must be numbers only')

        if len(tag_number) != 5:
            raise forms.ValidationError('Tag number must be five digits long')

        return tag_number

    def clean(self):
        """Sort out the tag number"""
        c_data = self.cleaned_data

        c_data['tree'] = None
        tag_number = c_data.get('tag_number')
        if tag_number:
            try:
                c_data['tree'] = Tree.objects.get(
                    tag_number=tag_number)
            except Tree.DoesNotExist:
                if self.user.is_authenticated():
                    # Then we can make a new tagged tree and attribute it to
                    # this user. ADAPT will verify.
                    tree = Tree.objects.create(
                        location=c_data.get('location'),
                        creator_email=self.user.email,
                        tag_number=tag_number
                    )
                    c_data['tree'] = tree

                    EmailTemplate.send('admin_new_tag',
                        tree=tree,
                        request=self.request,
                        this_tree_was='tagged from a new sighting',
                    )
                else:
                    self._errors["tag_number"] = self.error_class([(
                        "Hey! It looks like we haven't seen this tag number "
                        "yet. If you are trying to claim it, please log in "
                        "first!")])
        else:
            email = self.user.email if self.user.is_authenticated() else c_data['creator_email']
            c_data['tree'] = Tree.objects.create(
                location=c_data.get('location'),
                creator_email=email
            )
            EmailTemplate.send('new_untagged_tree',
                to_emails=[email],
                request=self.request,
            )


        return c_data


class AnonSightingForm(SightingForm):
    """Wraps up sightings by non-auth'd users."""

    class Meta:
        model = Sighting
        exclude = ('id', 'tree', 'created', 'modified')


class ClaimForm(forms.Form):
    tag_number = forms.CharField(max_length=5)
    image = forms.ImageField()

    def __init__(self, user, tree, *args, **kwargs):
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.user = user
        self.tree = tree

    def clean(self):
        """Make sure this is the same user that tagged it...."""
        if self.tree.creator_email != self.user.email:
            raise ValidationError(
                "It looks like you didn't tag this tree originally. "
                "Are you using the same email address?")
        return self.cleaned_data

