var due_date_cards = new Array();
var did_all_boards_return = null;
var checker_interval = null;
var username = "N/A";

function authorize()
{
    change_status("waiting to be authorized");
    Trello.authorize({type    : "popup",
                      expiration : "never",
                      success : after_authorize,  });
}

function after_authorize()
{
    change_status("authorized, getting trello data");
    
    //Get username:
    Trello.get("members/me", function(me, ix){
            username = me.username;
            send_data();
        });
}

function send_data()
{
    Dajaxice.theapp.process_cards(after_send, {"token" : Trello.token(), "username" : username})
    change_status("generating your feed - it might take a few seconds.");
}

function after_send(data){
    stop_status();
    if (data.error)
    {
        change_status("error generating feed: " + data.error);
        return;        
    }
    show_instructions(data.url);
}

function change_status(new_status)
{
    var spinner = "<img src='/img/ajax-loader.gif' />";
    $("#status_message").html(spinner + new_status);    
}

function stop_status()
{
    $("#status_message").html("All done.");
}

function show_instructions(url)
{
    var actual_url = "http://fun.sveder.com/feed/" + url;
    
    $("#feed_url").html("<input width=300 value='" + actual_url + "' />");
    $("#feed_url").click(function(){
            $("#feed_url>input").trigger('select');
        });
    
    $("div#instructions").fadeIn()
}