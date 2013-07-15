#!/usr/bin/env python
# -*- coding: utf-8 -*-
FLAGGED_MESSAGE = """
Dear ADAPT,

Someone has flagged %(the_item)s:

    %(url)s

You can hide it or un-flag it here:

    %(admin_url)s

The flagger's email address is: %(email)s

Have a good day!

"""


SIGHTING_MESSAGE = """
Dear AshTag Tagger,

An update was posted to your Tagged Tree.

You can see the update here:

    %(url)s

Please note, if the update is not for your tree, you can flag the update and it
will be removed.

Have a good day!

"""

NEW_TAG_MESSAGE = """
Dear ADAPT,

Someone has just added a tag number to a tree:

    %(url)s

You can reject this tag by selecting 'Reject this tag' in the admin list:

    %(admin_url)s

The tree was %(this_tree_was)s.

Have a good day!

"""
