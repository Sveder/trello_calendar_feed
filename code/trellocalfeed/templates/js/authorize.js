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

function filter_cards(boards)
{
    //Set up a listener to wait for all boards to return:
    checker_interval = setInterval(check_if_done, 5000);
    
    did_all_boards_return = boards.length;
    $.each(boards, function(ix, board){
        var cards_url = "/boards/" + board.id + "/cards";

        Trello.get(cards_url, function(ix, cards){
            did_all_boards_return -= 1;
            $.each(ix, function(ix, card) {
                if (card.due)
                {
                    //Check that the due time is in the definite future:
                    var due_date = new Date(card.due);
                    var now = new Date();
                    if (due_date > now)
                    {
                        due_date_cards.push(card);
                    }
                }
            });
        });
    });
    
}

function check_if_done(){
    if (did_all_boards_return === 0){
        send_cards();
        clearInterval(checker_interval);
        checker_interval = null;
    }
}

function after_authorize(){
    console.log("User authorized...");
    
    //Get username:
    Trello.get("members/me", function(me, ix){
            username = me.username;
        });
    
    //Get all cards with due date:    
    Trello.get("members/me/boards", filter_cards);
}

function send_cards(){
    var data = JSON.stringify(due_date_cards);
    Dajaxice.theapp.process_cards(after_send, {'cards_json': data, "token" : Trello.token(), "username" : username})
}

function after_send(data){
    due_date_cards = new Array();
    
    console.log("After send");
    console.log(data.url);
    window.location = "/feed/" + data.url;
}