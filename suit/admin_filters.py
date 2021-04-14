from django.utils.translation import gettext_lazy as _
from django.contrib.admin import FieldListFilter


class IsNullFieldListFilter(FieldListFilter):
    notnull_label = _('Is present')
    isnull_label = _('Is Null')

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)
        super(IsNullFieldListFilter, self).__init__(field,
                                                    request, params, model,
                                                    model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, cl):
        for lookup, title in (
                (None, _('All')),
                ('False', self.notnull_label),
                ('True', self.isnull_label),
        ):
            yield {
                'selected': self.lookup_val == lookup,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: lookup,
                }),
                'display': title,
            }
