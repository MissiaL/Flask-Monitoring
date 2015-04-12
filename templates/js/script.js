function blinker(tablename,key) {
    $('.'+tablename+'rev'+key).fadeOut(500);
    $('.'+tablename+'rev'+key).fadeIn(500);
}

function changeParamHeadTable(tablename,key,data) {
    var name=data[0]
    var ip=data[1]
    var port=data[2]
    var url=data[3]
    var rev=data[4]
    var stat=data[5]
    $('.'+tablename+'name'+key).text(name);
    $('.'+tablename+'url'+key).html("<a href="+'http://'+url+':'+port+'/'+url+">"+url+"")
    if (rev=='Uknown'){
        setInterval(blinker(tablename,key), 1000);
    }
    else {
    $('.'+tablename+'rev'+key).text(rev);
    }
    if (stat == 1) {
        $('.'+tablename+'status'+key).html("<p style="+'color:green;'+">"+'Online'+"");
    }
    else {
        $('.'+tablename+'status'+key).html("<p style="+'color:red;'+">"+'Offline'+"");
    }
    $('.'+tablename+'ip'+key).text(ip);
}

function changeResCamStatus(tablename,key, status) {
    if (status == 1) {
        $('.'+tablename+key).css("background-color", 'green');
    }
    else {
        $('.'+tablename+key).css("background-color", 'red');
    }
}

function test() {
    $(document).ready(
            function() {
                setInterval(function() {
                    $.getJSON("/js", function(data){
                        var ResStatus=data['jsResStatus']
                        var CamStatus=data['jsCamStatus']
                        var MergeStatus=data['jsMergeStatus']
                        var DocStatus=data['jsDocStatus']
                        var BuildStatus=data['jsBuildStatus']
                        var TestStatus=data['jsTestStatus']
                        $.each(ResStatus, function(key, status){
                            changeResCamStatus('res',key, status);
                        });
                        $.each(CamStatus, function(key, status){
                            changeResCamStatus('cam',key, status);
                        });
                        $.each(MergeStatus, function(key, data){
                            changeParamHeadTable('merge',key,data);
                        });
                        $.each(DocStatus, function(key, data){
                            changeParamHeadTable('doc',key,data);
                        });
                        $.each(BuildStatus, function(key, data){
                            changeParamHeadTable('build',key,data);
                        });
                        $.each(TestStatus, function(key, data){
                            changeParamHeadTable('test',key,data);
                        });
                    });

                },5000);
            });
};


test()