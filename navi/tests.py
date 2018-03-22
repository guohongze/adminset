#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create your tests here.
from django.test import TestCase, Client


class NaviTest(TestCase):
    def test_index(self):
        self.client = Client(enforce_csrf_checks=True)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
