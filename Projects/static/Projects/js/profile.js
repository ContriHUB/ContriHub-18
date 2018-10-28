$(document).ready(function() {
  $(".prs_pending").hide();
  $(".prs_vclosed").hide();

  $(document).on('click',".vclose,.unvclose",function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ppr");
    var pr_id = $(".pr_info",pr).attr("pr-id");
    var csrf = $(".ppr").attr("csrf");
    console.log(pr);
    // $(".process",this).show();
    //alert($("#bonus").val())
    var bonus_pts = $("#bonus",pr).val();
    var deduct_pts = $("#deduct",pr).val();
    console.log(pr_id)
    console.log('bonus_pts - '+bonus_pts)
    console.log('deduct_pts - '+deduct_pts)
    if(bonus_pts=='') bonus_pts=0;
    if(deduct_pts=='') deduct_pts=0;

    $.ajax({
      url: "response_pr",
      data: {
        pr_id: pr_id,
        bonus_pts: bonus_pts,
        deduct_pts: deduct_pts,
        csrfmiddlewaretoken: csrf
      },
      type: "post",
      cache: false,
      beforeSend: function() {
        // $(".request").html('<i class="fa fa-spinner fa-spin fa-1x"></i>');
        //$(".process",this).show();
      },
      success: function(data) {
        if (data == "success") {
          // alert("Successfully updated the status of this Pull Request");
          if($('body').find('#alert-modal').length <= 0) {
            $('body').append('<div id="alert-modal"></div>');
          }
          $('#alert-modal').html("<p>Successfully updated the status of this Pull Request</p>");
          $('#alert-modal').modal();
          //alert(data);
          // document.location.reload();
          $(pr).hide();
        }
      },  
      afterSend: function() {
        // $(".request").html(' request for verification ');
        // $(".process",this).hide();
      }
    });
  });

  $(document).on("click",".delete",function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ppr");
    var that=$(this).prev('.ppr');
    var pr_id = $(".pr_info", pr).attr("pr-id");
    var csrf = $(".ppr").attr("csrf");
    console.log("pr_id " + pr_id);
    $.ajax({
      url: "remove_pr",
      data: {
        pr_id: pr_id,
        csrfmiddlewaretoken: csrf
      },
      type: "post",
      cache: false,
      beforeSend: function() {
        //alert("Requesting server ...");
      },
      success: function(data) {
        if (data) {
          // alert(data);
          if ($('body').find('#alert-modal').length <= 0) {
            $('body').append('<div id="alert-modal"></div>');
          }
          $('#alert-modal').html(`<p>${data}</p>`);
          $('#alert-modal').modal();
          $(pr).hide();
        }
      }
    });
  });

  $(".all").click(function() {
    $(".issues_all").show();
    $(".prs_pending").hide();
    $(".prs_vclosed").hide();
  });

  $(".pending").click(function() {
    $(".prs_pending").show();
    $(".issues_all").hide();
    $(".prs_vclosed").hide();
  });

  $(".vclosed").click(function() {
    $(".prs_vclosed").show();
    $(".prs_pending").hide();
    $(".issues_all").hide();
  }); 

  $(".nvclosed").click(function() {
    $(".prs_pending").hide();
    $(".issues_all").hide();
    $(".prs_vclosed").hide();
  });

  $(".nattempted").click(function() {
    $(".prs_pending").hide();
    $(".issues_all").hide();
    $(".prs_vclosed").hide();
  }); 

});
