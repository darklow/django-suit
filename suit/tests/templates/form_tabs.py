from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from suit.tests.mixins import ModelsTestCaseMixin, UserTestCaseMixin
from suit.tests.models import Book, BookAdmin, test_app_label

app_label = test_app_label()


class TabbedBookAdmin(BookAdmin):
    list_filter = ('id', 'name',)
    suit_form_tabs = (('tab1', 'Tab1'), ('tab2', ugettext('Tab2')))
    suit_form_includes = None


admin.site.unregister(Book)
admin.site.register(Book, TabbedBookAdmin)


class FormTabsTestCase(ModelsTestCaseMixin, UserTestCaseMixin):
    def setUp(self):
        self.login_superuser()
        self.url = reverse('admin:%s_book_add' % app_label)
        self.get_response(self.url)

    def test_tabs_appearance(self):
        for x in range(0, 2):
            vars = (TabbedBookAdmin.suit_form_tabs[x][0],
                    TabbedBookAdmin.suit_form_tabs[x][1])
            self.assertContains(self.response, '<li><a href="#%s">%s</a></li>' %
                                               vars)

    def test_template_includes(self):
        suit_form_include = 'admin/date_hierarchy.html'
        TabbedBookAdmin.suit_form_includes = (
            (suit_form_include, 'top', 'tab1'),
        )
        self.get_response(self.url)
        self.assertTemplateUsed(self.response,
                                'suit/includes/change_form_includes.html')
        self.assertTemplateUsed(self.response, suit_form_include)
        self.assertContains(self.response,
                            '<div class="suit-include suit-tab suit-tab-tab1">')
