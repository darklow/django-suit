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
        ParentItem('Right Side Menu', children=[
            ChildItem('Password change', url='admin:password_change'),
            ChildItem('Open Google', url='http://google.com', target_blank=True),

        ], align_right=True),
    )
