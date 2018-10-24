$(document).ready(function() {
  $(".process").hide();
  $(".prs_pending").hide();
  $(".prs_nattempted").hide();
  $(".prs_vclosed").hide();
  $(".prs_unvclosed").hide();

  $(".vclose,.unvclose").click(function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ppr");
    var pr_id = $(".pr_info", pr).attr("pr-id");
    var csrf = $(".ppr").attr("csrf");
    // $(".process",this).show();

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

  $(".delete").click(function(e) {
    e.preventDefault();
    var pr = $(this).closest(".ind_pr");
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
          alert(data);
          document.location.reload();
        }
      }
    });
  });

  $(".all").click(function() {
    $(".issues_all").show();
    $(".prs_pending").hide();
    $(".prs_nattempted").hide();
    $(".prs_vclosed").hide();
    $(".prs_unvclosed").hide();
  });

  $(".pending").click(function() {
    $(".prs_pending").show();
    $(".issues_all").hide();
    $(".prs_nattempted").hide();
    $(".prs_vclosed").hide();
    $(".prs_unvclosed").hide();
  });

  $(".vclosed").click(function() {
    $(".prs_vclosed").show();
    $(".prs_pending").hide();
    $(".issues_all").hide();
    $(".prs_nattempted").hide();
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

});
