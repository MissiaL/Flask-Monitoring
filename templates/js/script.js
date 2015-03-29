function show() {
    var count = 0;
    $("#js").click(function(){
        $.getJSON("/js", function(result){

            $.each(result, function(i, field){
                //$("#divjs").append(field[0] + " ");

                $("#divjs").append(field[count][0] + " ");
                count+=1;
            });
        });
    });
}

$(document).ready(function(){
    show();
//    setInterval('show()',1000);
});