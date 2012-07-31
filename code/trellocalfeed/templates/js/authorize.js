var due_date_cards = new Array();
var did_all_boards_return = null;
var checker_interval = null;
var username = "N/A";

function authorize()
{
    console.log("Starting to authorize...");
    Trello.authorize({type    : "popup",
                      expiration : "never",
                      success : after_authorize,  });
}

function after_authorize(){
    console.log("User authorized...");
    
    //Get username:
    Trello.get("members/me", function(me, ix){
            username = me.username;
            send_data();
        });
}

function send_data(){
    Dajaxice.theapp.process_cards(after_send, {"token" : Trello.token(), "username" : username})
}

function after_send(data){
    due_date_cards = new Array();
    
    console.log("After send");
    console.log(data.url);
    console.log(data.error);
}