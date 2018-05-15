from django import get_version
from django.apps import AppConfig
from django.contrib.admin.options import ModelAdmin
from . import VERSION

ALL_FIELDS = '__all__'

# Form row sizing as Bootstrap CSS grid classes: (for label, for field column)
SUIT_FORM_SIZE_LABEL = 'col-xs-12 col-sm-3 col-md-2'
SUIT_FORM_SIZE_INLINE = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-9 col-md-10 form-inline')
SUIT_FORM_SIZE_SMALL = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-6 col-md-5 col-lg-4')
SUIT_FORM_SIZE_HALF = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-7 col-md-6 col-lg-5')
SUIT_FORM_SIZE_LARGE = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-8 col-md-7 col-lg-6')
SUIT_FORM_SIZE_X_LARGE = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-9 col-md-8 col-lg-7')
SUIT_FORM_SIZE_XX_LARGE = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-9 col-md-10 col-lg-8')
SUIT_FORM_SIZE_XXX_LARGE = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-9 col-md-10 col-lg-9')
SUIT_FORM_SIZE_FULL = (SUIT_FORM_SIZE_LABEL, 'col-xs-12 col-sm-9 col-md-10')


class DjangoSuitConfig(AppConfig):
    name = 'suit'
    verbose_name = 'Django Suit'
    django_version = get_version()
    version = VERSION

    # Menu and header layout - horizontal or vertical
    layout = 'horizontal'

    # Set default list per page
    list_per_page = 20

    # Show changelist top actions only if any row is selected
    toggle_changelist_top_actions = True

    # Define menu
    #: :type: list of suit.menu.ParentItem
    menu = []

    # Automatically add home link
    menu_show_home = True

    # Define callback / handler to change menu before it is getting rendered
    menu_handler = None

    # Enables two column layout for change forms with submit row on the right
    form_submit_on_right = True

    # Hide name/"original" column for all tabular inlines.
    # May be overridden in Inline class by suit_form_inlines_hide_original = False
    form_inlines_hide_original = False

    # For size
    form_size = {
        'default': SUIT_FORM_SIZE_X_LARGE,
        # 'fields': {}
        'widgets': {
            'RelatedFieldWidgetWrapper': SUIT_FORM_SIZE_XXX_LARGE
        }
        # 'fieldsets': {}
    }

    # form_size setting can be overridden in ModelAdmin using suit_form_size parameter
    #
    # Example:
    # ----------------------------------------------
    # suit_form_size = {
    #     'default': 'col-xs-12 col-sm-2', 'col-xs-12 col-sm-10',
    #     'fields': {
    #          'field_name': SUIT_FORM_SIZE_LARGE,
    #          'field_name2': SUIT_FORM_SIZE_X_LARGE,
    #      },
    #      'widgets': {
    #          'widget_class_name': SUIT_FORM_SIZE_FULL,
    #          'AdminTextareaWidget': SUIT_FORM_SIZE_FULL,
    #      },
    #      'fieldsets': {
    #          'fieldset_name': SUIT_FORM_SIZE_FULL,
    #          'fieldset_name2': SUIT_FORM_SIZE_FULL,
    #      }
    # }

    def __init__(self, app_name, app_module):
        self.setup_model_admin_defaults()
        super(DjangoSuitConfig, self).__init__(app_name, app_module)

    def ready(self):
        super(DjangoSuitConfig, self).ready()

    def setup_model_admin_defaults(self):
        """
        Override some ModelAdmin defaults
        """
        if self.toggle_changelist_top_actions:
            ModelAdmin.actions_on_top = True
        ModelAdmin.actions_on_bottom = True

        if self.list_per_page:
            ModelAdmin.list_per_page = self.list_per_page
