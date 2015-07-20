# coding=utf-8
from __future__ import unicode_literals

ACTION = """
<a class="btn btn-primary" href="#myModal{id}" onclick="javascript:$('#conteneur{id}').load('{url}',function(e){{$('#myModal{id}').modal('show');}});">Changer les infos paiements</a>
<div id="conteneur{id}"></div>
"""

DOSSIER_INCOMPLET = """
<a class="btn btn-primary"
   href="#myModalIncomplet{id}"
   onclick="javascript:$('#conteneurIncomplet{id}').load('{url}',function(e){{$('#myModalIncomplet{id}').modal('show');}});">
   Dossier incomplet
</a>
<div id="conteneurIncomplet{id}"></div>
"""