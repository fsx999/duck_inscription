# coding=utf-8
from __future__ import unicode_literals
ACTION = """
<form id="form{id}" class="form-horizontal" action="{url}{id}" method="post">
</form>
"""
# ACTION = """
# <!-- Button trigger modal -->
# <a class="btn btn-primary" href="#myModal{id}" onclick="javascript:$('#myModal{id} .modal-body').load('{url}',function(e){{$('#myModal{id}').modal('show');}});">Changer de centre</a>
# <!-- Modal -->
# <div class="modal fade" id="myModal{id}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel{id}" aria-hidden="true">
#   <div class="modal-dialog">
#
#     <div class="modal-content">
#     <form id="form{id}" class="form-horizontal" action="{url}{id}" method="post">
#       <div class="modal-header">
#         <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
#         <h4 class="modal-title" id="myModalLabel{id}">Changement du centre de gestion</h4>
#       </div>
#
#       <div class="modal-body">
#
#       </div>
#
#       <div class="modal-footer">
#         <button type="button" class="btn btn-default" data-dismiss="modal">Fermer</button>
#       </div>
#       </form>
#     </div>
#
#   </div>
# </div>
# """
