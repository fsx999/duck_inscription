
from django.template import loader
from django.utils.text import capfirst
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.translation import ugettext as _

from xadmin.sites import site
from xadmin.filters import SEARCH_VAR
from xadmin.views import BaseAdminPlugin, CommAdminView


class IEDPlugin(BaseAdminPlugin):
    urls = [
        {'name': 'Wiki', 'url': 'wiki'},
        {'name': 'Forum', 'url': 'forum'},
    ]


    def get_context(self, context):
        return context

    # Block Views
    def block_top_navbar(self, context, nodes):
        nodes.append(
            loader.render_to_string('xadmin_plugins/comm.top.lien.html', {'urls': self.urls}))




site.register_plugin(IEDPlugin, CommAdminView)
