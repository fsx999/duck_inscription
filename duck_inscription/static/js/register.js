$(document).ready(function() {
	if ($("input:checked").length != 0){
		$('.register').show();
		$('#e1s1').hide();
	}
	else{
		$('.register').hide();
	}
	$('#bouton_enregistrement').click(function(){
		if($("input:checked").length != 0){
			$('#e1s1').hide();
			$('.register').show();
		}
		else{
			//$("#erreur_validation").html("Vous devez accepter les conditions ci-dessus.");
            $('#div_id_tos').addClass("error");
            if($("#error_id_tos").length==0)
                $('#div_id_tos > .controls').append('<span class="help-block" id="error_id_tos">Vous devez accepter les conditions ci-dessus.</span>');
		}
	});
    $('#id_tos').click(function(){
       if($('#id_tos:checked').val()=='on'){
            $('#error_id_tos').remove();
       }
    });

    $.validator.addMethod(
        "regex",
        function(value, element, regexp) {
            var check = false;
            return this.optional(element) || regexp.test(value);
        },
        "Ce champ ne doit contenir que des lettres, des chiffres et des underscores ( _ )."
    );

    $("#form_registration").validate({
        rules: {
            username:{
                required:true,
//                test_user:true,
                remote:'/test_user/',
                minlength:5,
                regex:/^\w+$/
            },
            password1:{
                minlength:4,
                required: true
            },
            password2:{
                equalTo:"#id_password1"

            },
            email:{
                required:true,
                email:true,
                remote:'/test_email/'
            },
            email1:{
                equalTo:"#id_email"
            }
        },
        messages:{
            username:{
                remote:jQuery.validator.format("Cet identifiant est déjà utilisé")
            },
            email:{
                remote:jQuery.validator.format("Cet email est déjà utilisé")
            }
        }

    });

});