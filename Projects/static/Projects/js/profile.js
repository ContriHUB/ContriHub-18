$(document).ready(function() {
  $(".process").hide();
  $(".pending_prs").hide();
  $(".prs_nattempted").hide();
  $(".verified_prs").hide();
  $(".prs_unvclosed").hide();

  $(".vclose,.unvclose").click(function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ppr");
    var pr_id = $(".pr_info", pr).attr("pr-id");
    var csrf = $(".ppr").attr("csrf");
    // $(".process",this).show();
    console.log("csrf = "+csrf);
    $.ajax({
      url: "response_pr",
      data: {
        pr_id: pr_id,
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
          alert("Successfully updated the status of this Pull Request");
          //alert(data);
          document.location.reload();
        }
      },
      afterSend: function() {
        // $(".request").html(' request for verification ');
        // $(".process",this).hide();
      }
    });
  });






$(".pending").click(function(e) {
    e.preventDefault();
    dataType:'json',
    $.ajax({
      url: "ajax_fetch",
      data: {
       'status':2,
       'username':username,

      },
      type: "get",
      cache: false,

      success: function(data) {

       $(".pending_prs").html(data);
       $(".pending_prs").show();
       $(".issues_all").hide();
       $(".verified_prs").hide();
      },

    });
  });



$(".vclosed").click(function(e) {
    e.preventDefault();
    dataType:'json',
    $.ajax({
      url: "ajax_fetch",
      data: {
       'status':3,
       'username':username,


      },
      type: "get",
      cache: false,

      success: function(data) {

       $(".verified_prs").html(data);
       $(".verified_prs").show();
       $(".issues_all").hide();
       $(".pending_prs").hide();
      },

    });
  });



  $(".all").click(function() {
    $(".issues_all").show();
    $(".pending_prs").hide();
    $(".prs_nattempted").hide();
    $(".verified_prs").hide();
    $(".prs_unvclosed").hide();
  });

  $(".nvclosed").click(function() {
    $(".prs_unvclosed").show();
    $(".prs_pending").hide();
    $(".issues_all").hide();
    $(".prs_nattempted").hide();
    $(".prs_vclosed").hide();
  });

  $(".nattempted").click(function() {
    $(".prs_nattempted").show();
    $(".prs_pending").hide();
    $(".issues_all").hide();
    $(".prs_vclosed").hide();
    $(".prs_unvclosed").hide();
  });

  $(".delete").click(function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ppr");
    var pr_id = $(".pr_info", pr).attr("pr-id");
    var csrf = $(".ppr").attr("csrf");
    console.log("pr_id " + pr_id);
    console.log("csrf = "+csrf);
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
          alert(data);
          document.location.reload();
        }
      }
    });
  });
});
