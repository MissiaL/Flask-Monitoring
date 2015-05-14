$(document).ready(function() {
    $("#next").click(function(){
        var svnBranch = $('#svnBranch').val();
        var svnTesting = $('#svnTesting').val();
        if (svnBranch)
//        $.post( "branch.html", { branch: svnBranch, testing: svnTesting } );

        $.ajax({
            type: 'POST',
            // Provide correct Content-Type, so that Flask will know how to process it.
            contentType: 'application/json',
            // Encode your data as JSON.
            data: JSON.stringify([svnBranch,svnTesting]),
            // This is the type of data you're expecting back from the server.
            dataType: 'json',
            url: '/jsbranch',
            success: function (e) {
                console.log(e);
            }
        });
    });
});