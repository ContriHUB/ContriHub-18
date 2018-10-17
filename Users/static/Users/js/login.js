$(document).ready(function(){
        $(".signup_text").click(function () {
            $(".signin").hide(); //$("#human").removeClass('bottom');
            $(".signup").show();  //$("#product").addClass('bottom');
        });
        
        $(".signin_text").click(function () {
            $(".signup").hide(); //  $("#product").removeClass('bottom');
            $(".signin").show();  // $("#human").addClass('bottom');
        });

        $('select').formSelect();
    }) 
