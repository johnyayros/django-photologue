#!/usr/bin/env python
# -*- coding: utf-8 -*-
from photologue.tests.factories import PhotoFactory
from photologue.models import Photo
from django.test import TestCase


class RequestPhotoTest(TestCase):

    urls = 'photologue.tests.test_urls'

    def setUp(self):
        super(RequestPhotoTest, self).setUp()
        self.photo = PhotoFactory(title_slug='fake-photo')

    def tearDown(self):
        super(RequestPhotoTest, self).tearDown()
        self.photo.delete()

    def test_archive_photo_url_works(self):
        response = self.client.get('/ptests/photo/')
        self.assertEqual(response.status_code, 200)

    def test_archive_photo_empty(self):
        """If there are no photo to show, tell the visitor - don't show a
        404."""

        Photo.objects.all().update(is_public=False)

        response = self.client.get('/ptests/photo/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['latest'].count(),
                         0)

    def test_paginated_photo_url_works(self):
        response = self.client.get('/ptests/photo/page/1/')
        self.assertEqual(response.status_code, 200)

    def test_photo_works(self):
        response = self.client.get('/ptests/photo/fake-photo/')
        self.assertEqual(response.status_code, 200)


    def test_archive_year_photo_works(self):
        response = self.client.get('/ptests/photo/2011/')
        self.assertEqual(response.status_code, 200)

    def test_archive_month_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/')
        self.assertEqual(response.status_code, 200)

    def test_archive_day_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/23/')
        self.assertEqual(response.status_code, 200)


    def test_detail_photo_works(self):
        response = self.client.get('/ptests/photo/2011/dec/23/fake-photo/')
        self.assertEqual(response.status_code, 200)
