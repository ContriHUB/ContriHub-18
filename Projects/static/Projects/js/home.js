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
                        // alert(data);
                        $("#snackbar").html(data);
                        showMessage();
                        $(issue).hide();
                    }
                }
            });
        });

    $(document).on('click', ".edit_issue", function (e) {
        e.preventDefault();

        var issue = $(this).closest('.single-issue');

        var title_issue = $(".issue-info", issue).text();
        var link_issue = $(".issue-info", issue).attr("href");
        var title_project = $(".project-info", issue).text();
        var link_project = $(".project-info", issue).attr("href");
        var issue_id = $(".issue-info", issue).attr("issue-id");
        var mentor_name = $(".issue_mentor",issue).text();
        var points=$(".issue_points",issue).text();
        var level=$(".issue_level",issue).text();

        console.log(issue_id)
        title_issue = title_issue.trim();
        link_issue = link_issue.trim();
        title_issue = title_issue.trim();
        link_project = link_project.trim();
        mentor_name=mentor_name.trim();
        points=points.trim();
        level=level.trim();

        points=points.slice(18);
        if(level[8]=='E')
        level='1';
        else if(level[8]=='M')
        level='2';
        else
        level='3';

        $(".modal-title").html("Edit Issue")
        $("#mode").attr("value", "1"); //changing to edit mode
        $("#issue_id").attr("value", issue_id);

        $("#issue_mentor").val(mentor_name);

        $("#issue_title").val(title_issue);

        $("#issue_link").val(link_issue);

        $("#project_title").val(title_project);

        $("#project_link").val(link_project);
        $("#level").val(level);
        $("#points").val(points);
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

function showMessage() {
        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function () { x.className = x.className.replace("show", ""); }, 3000);
    }
