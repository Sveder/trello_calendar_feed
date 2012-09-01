//Generate instructions for the user
function show_instructions(url, boards)
{
    console.log("Hayush");
    console.log(boards);
    
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
    
    console.log(is_only_assigned);
    console.log(is_all_day);
    console.log(meeting_length);
    console.log(boards);
    
    Dajaxice.theapp.create_feed(after_feed_created, {"is_only_assigned" : is_only_assigned,
                                             "all_day_meeting" : is_all_day,
                                             "meeting_length" : meeting_length,
                                             "boards" : boards})
}

function after_feed_created(data)
{
    console.log("loler");
    console.log(data);
   
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

