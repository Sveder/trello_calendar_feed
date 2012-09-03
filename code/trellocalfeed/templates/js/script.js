//Generate instructions for the user
function show_instructions(url, boards)
{
    var actual_url = "http://fun.sveder.com/feed/" + url;
    
    $("#feed_url").html("<input width=300 value='" + actual_url + "' />");
    $("#feed_url").click(function(){
            $("#feed_url>input").trigger('select');
        });
    
    $("div#instructions").fadeIn()
}

function create_feed()
{
    //Get general options:
    var is_only_assigned = $('#is_feed_assigned_to_me').is(':checked');
    var is_all_day = $('#all_day_meeting').is(':checked');
    var meeting_length = $('#meeting_length').val();
    
    //Get list of boards:
    var boards = new Array();
    $(".board:checkbox:checked.board").each(function()
    {
        boards.push($(this)[0].id);
    });
    
    Dajaxice.theapp.create_feed(after_feed_created, {"is_only_assigned" : is_only_assigned,
                                             "all_day_meeting" : is_all_day,
                                             "meeting_length" : meeting_length,
                                             "boards" : boards});
}

//Show fancybox with the info to subscribe to a feed:
function after_feed_created(data)
{
    if (data.error)
    {
        alert(data.error);
        return;        
    }
    
    var actual_url = "http://fun.sveder.com/feed/" + data.feed_url;
    
    $("#feed_url").html("<input width=300 value='" + actual_url + "' />");
    $("#feed_summary").html("Feed summary: " + data.feed_summary);
    
    $("#feed_url").click(function(){
            $("#feed_url>input").trigger('select');
        });
    
    
    $("a#new_feed_fancy").fancybox({
              'transitionIn'	:	'fade',
              'transitionOut'	:	'fade',
              'speedIn'	:	400, 
              'speedOut'	:	200,
      });
    $("a#new_feed_fancy").click();
    
    var feed_id = data.feed_id;
    var new_line = '<div class="new_feed_item" id="feed_' + feed_id + '">'
    new_line += '<div id="url_' + feed_id + '"><a href=/feed/' + data.feed_url + '>' + data.feed_url.substr(0, 10) + '...</a></div>';
    new_line += '<div>' + data.feed_summary + '</div>';
    new_line += '<div><button class="delete_button" id="del_' + feed_id + '" onclick="confirm_feed_delete(' + feed_id + ');">Delete Feed</button></div>';
    new_line += '</div>';
    
    $(".feeds_list").append(new_line);
    
}

function toggle_all_day(){
    var is_all_day = $('#all_day_meeting').is(':checked');
    
    if (is_all_day === true)
    {
        $("#meeting_length").attr('disabled', true);
    }
    else
    {
        $("#meeting_length").attr('disabled', false);
    }
}

function toggle_all_boards()
{
    $(".board").each(function()
    {
        $(this).attr("checked", !$(this).attr("checked"));
    });    
}


//Ask whether to delete feed or not:
function confirm_feed_delete(feed_id)
{
    var should_delete = confirm("Are you sure you want to delete the feed? You can always recreate it later, but all applications that are subscribed to it will stop showing new events.")
    if (should_delete)
    {
        delete_feed(feed_id);
    }
}

function delete_feed(feed_id)
{
    Dajaxice.theapp.delete_feed(after_delete, {"feed_id" : feed_id});
}

function after_delete(data)
{
    if (!data.deleted)
    {
        console.log(data.error);
        return;
    }
    
    //Strike through to indicate deleted:
    $("#feed_" + data.feed_id).css('text-decoration', 'line-through');
    //Disable the delete button:
    $("#del_" + data.feed_id).attr('disabled', true);
    //Add a message that the feed was deleted:
    $("#url_" + data.feed_id).html("[deleted]");
}

function add_email()
{
    var email = $("#email_text").val();
    Dajaxice.theapp.add_email(after_add_email, {"email" : email});
}

function after_add_email(data)
{
    if (data.error)
    {
        alert(data.error);
    }
    console.log("email added");
}