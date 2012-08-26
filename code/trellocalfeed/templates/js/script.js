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
