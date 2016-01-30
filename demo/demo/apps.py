from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    menu = (
        ParentItem('Content', children=[
            ChildItem(model='demo.country'),
            ChildItem(model='demo.continent'),
        ]),
        ParentItem('Users', children=[
            ChildItem(model='auth.user'),
            ChildItem('User groups', 'auth.group'),
            ChildItem('Custom page', url='/admin/custom/'),
        ]),
        ParentItem('Configuration', children=[
            ChildItem('Custom page', url='/admin/custom/'),

        ], align_right=True),
    )
