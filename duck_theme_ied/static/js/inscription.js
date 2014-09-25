/**
 * Created by paul on 18/06/14.
 */
(function ($) {
    $(document).ready(function () {
        function toggle_motif() {
            if (['accepte', 'complet', undefined].indexOf($("input[name='choix']:checked").val()) >= 0) {
                $('#div_id_motif').hide();
            }
            else {
                $('#div_id_motif').show();
            }
        }

        toggle_motif();
        $('[name=choix]').change(function () {
            toggle_motif();
        });
        $("#id_code_dossier").val("").focus();
    });

})(jQuery);
