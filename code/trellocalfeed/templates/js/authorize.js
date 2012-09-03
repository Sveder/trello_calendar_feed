var due_date_cards = new Array();
var did_all_boards_return = null;
var checker_interval = null;

//Ask the trello client to authorize us
function authorize()
{
    _gaq.push(['_trackEvent', "Authorize", 'clicked', ""]);

    change_status("waiting to be authorized");
    Trello.authorize({type    : "popup",
                      expiration : "never",
                      success : after_authorize,
                      name : "Trello to calendar feed"});
}

//Ask trello to get some user details for us:
function after_authorize()
{
    change_status("authorized, getting trello data");
    
    //Get username:
    Trello.get("members/me", function(me, ix){
            var username = me.username;
            var userid = me.id;
            send_data(username, userid);
        });
}

//Send the user data using ajax/dajaxice to the server:
function send_data(username, userid)
{
    var email = $("#email_text").val();
    Dajaxice.theapp.process_cards(after_send, {"token" : Trello.token(), "username" : username, "userid" : userid, "email" : email})
    change_status("generating your feed - it might take a few seconds.");
}

//If there is an error show it, if not go to the user_url:
function after_send(data){
    stop_status();
    if (data.error)
    {
        change_status("error generating feed: " + data.error);
        return;        
    }
    
    window.location.href = "/user/" + data.user_url;
}

//Change the status indicator under the authorize button to a new message:
function change_status(new_status)
{
    var spinner = "<img src='/img/ajax-loader.gif' />";
    $("#status_message").html(spinner + new_status);    
}

function stop_status()
{
    $("#status_message").html("All done. Redirecting to the user console.");
}