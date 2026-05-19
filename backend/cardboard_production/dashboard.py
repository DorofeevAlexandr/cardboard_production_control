from __future__ import unicode_literals
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard


class CustomPagesModule(modules.DashboardModule):
    title = 'Тестовые страницы'
    template = 'admin/test_pages_dashboard.html'

    def is_empty(self):
        return False

    def init_with_context(self, context):
        if self._initialized:
            return

        self._initialized = True


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(
            modules.ModelList(
                title='Система управления содержимым',
                models=('cms.models.pagemodel.Page', )
            ))

        self.children.append(CustomPagesModule())


class CustomAppIndexDashboard(AppIndexDashboard):
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)
        self.children += [modules.ModelList(self.app_title, self.models), ]

    def init_with_context(self, context):
        return super(CustomAppIndexDashboard, self).init_with_context(context)