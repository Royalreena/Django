$('.openDiv').click(function () {       
        alert(1)     
        var id = $(this).attr('id');  
        var csrf_token = $("#csrf_token").val();
        $.ajax({ 
           data:{
                csrfmiddlewaretoken: ('{{csrf_token}}'),   
               // form:form.serialize(),            
                id:id,
                
                },
        type:'POST',
        url: '/setting/save-reporter/',
        success: function() {
            $('#authorisedreporter').show();
        }
      });
     });
