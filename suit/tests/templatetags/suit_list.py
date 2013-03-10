from django.contrib.admin import ModelAdmin
from django.core.urlresolvers import reverse
from suit.templatetags.suit_list import paginator_number, paginator_info, \
    pagination, suit_list_filter_select
from suit.tests.mixins import UserTestCaseMixin, ModelsTestCaseMixin
from suit.tests.models import Book


class SuitListTestCase(UserTestCaseMixin, ModelsTestCaseMixin):
    changelist = None
    book = None

    def get_changelist(self):
        self.get_response(reverse('admin:tests_book_changelist'))
        self.changelist = self.response.context_data['cl']

    def setUp(self):
        self.login_superuser()
        self.book = Book(name='Test')
        self.book.save()
        self.get_changelist()

    def test_paginator_number(self):
        output = paginator_number(self.changelist, 100)
        self.assertTrue('100' in output)

        output = paginator_number(self.changelist, '.')
        self.assertTrue('...' in output)

        output = paginator_number(self.changelist, 0)
        self.assertTrue('active' in output)

    def test_paginator_info(self):
        output = paginator_info(self.changelist)
        self.assertEqual('1 - 1', output)

    def test_pagination_one_page(self):
        pg = pagination(self.changelist)
        self.assertEqual(pg['cl'], self.changelist)
        self.assertEqual(pg['page_range'], [])
        self.assertEqual(pg['pagination_required'], False)

    def test_pagination_many_pages(self):
        per_page_original = ModelAdmin.list_per_page
        ModelAdmin.list_per_page = 20
        for x in range(25):
            book = Book(name='Test %d' % x)
            book.save()

        self.get_changelist()
        pg = pagination(self.changelist)
        ModelAdmin.list_per_page = per_page_original
        self.assertEqual(pg['cl'], self.changelist)
        self.assertEqual(pg['page_range'], [0, 1])
        self.assertEqual(pg['pagination_required'], True)

    def test_suit_list_filter_select(self):
        filter_matches = (self.book.pk, self.book.name)
        self.assertEqual(len(self.changelist.filter_specs), 2)
        for i, spec in enumerate(self.changelist.filter_specs):
            filter_output = suit_list_filter_select(self.changelist, spec)
            self.assertTrue('value="%s"' % filter_matches[i] in filter_output)
