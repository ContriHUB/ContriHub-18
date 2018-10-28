$(document).on("ready",function () {
    $(document).on('click',".delete",function (e) {
        e.preventDefault();

        var issue = $(this).closest('.single-issue');
        var issue_id = $(".issue-info", issue).attr('issue-id');
        var csrf = $(".single-issue").attr('csrf');
        $.ajax({
            url: 'remove_issue',
            data: {
                'issue_id': issue_id,
                'csrfmiddlewaretoken': csrf,
            },
            type: 'post',
            cache: false,
            beforeSend: function () {
                // alert("Requesting server ...")
            },
            success: function (data) {
                if (data) {
                    alert(data);
                    $(issue).hide();
                }
            }
        });
    });

    $(document).on('click',".change-label", function(e) {
        e.preventDefault();
        var issue = $(this).closest('.single-issue');
        var issue_id = $(".issue-info", issue).attr('issue-id');
        var csrf = $(".single-issue").attr('csrf');
        $.ajax({
            url: 'change_label',
            data: {
                'issue_id': issue_id,
                'csrfmiddlewaretoken': csrf,
            },
            type: 'post',
            cache: false,
            beforeSend: function () {
                // alert("Requesting server ...")
            },
            success: function (data) {
                if (data) {
                    //alert(data);
                    //console.log(issue)
                    var status = $(".pull-right",issue).html();
                    console.log(status);
                    if(status=="OPEN")
                    {
                        $(".change-label", issue).html("CLOSED");
                        $(".change-label", issue).attr("class","closed change-label pull-right");
                    }
                    else
                    {
                        $(".change-label", issue).html("OPEN");
                        $(".change-label", issue).attr("class", "open change-label pull-right");
                    }
                }

            }
        });
    });

    var infiniteScroll = new Waypoint.Infinite({
        element: $('.issues-container')[0],
        items: '.issue-list-item',
        //loadingClass: 'more-issues-loading',
        more: '.more-issues-link',
        onBeforePageLoad: function () {
            $('.more-issues-loading').show();

        },
        onAfterPageLoad: function () {
            $('.more-issues-loading').hide();
        }
    });

    $(document).on('click','.upVote',function (e) {
        e.preventDefault();
        var that = this
        var next = $(this).next('.btn')//Since The downvote button is after upvote
        var type = $(this).attr('voting_type');
        var issue = $(this).closest('.single-issue');
        var issue_id = $(".issue-info", issue).attr('issue-id');
        console.log(type);

        $.ajax({
            url: 'vote',
            data: {
                'issue_id': issue_id,
                'type': type,
            },
            dataType: 'json',
            type: 'get',
            cache: false,
            success: function (data) {
                // $('.upV').html(data.upvotes_count);
                $(that).html('<i class="fa fa-2x fa-thumbs-up"></i> &nbsp;' + data.upvotes_count);
                $(next).html('<i class="fa fa-2x fa-thumbs-down"></i> &nbsp;' + data.downvotes_count);
            }
        });
    });

    $(document).on('click','.downVote',function (e) {
        e.preventDefault();
        var that = this;
        var prev = $(this).prev('.btn')//Since The upvote button is before downvote
        var type = $(this).attr('voting_type');
        var issue = $(this).closest('.single-issue');
        var issue_id = $(".issue-info", issue).attr('issue-id');
        console.log(type);

        $.ajax({
            url: 'vote',
            data: {
                'issue_id': issue_id,
                'type': type,
            },
            dataType: 'json',
            type: 'get',
            cache: false,
            success: function (data) {

                $(that).html('<i class="fa fa-2x fa-thumbs-down"></i> &nbsp;' + data.downvotes_count);
                $(prev).html('<i class="fa fa-2x fa-thumbs-up"></i> &nbsp;' + data.upvotes_count);

            }
        });


    });

});