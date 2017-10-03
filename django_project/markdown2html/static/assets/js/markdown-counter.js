var needMatch = ['theorem', 'claim', 'corollary', 'def']
var counters = [0,0,0,0]
var tags = ['h3','h3','h3','h3']
var previous = 0;
$(document).ready(function(){
    var note_number = $("#theorem-counter").text();
    $(".markdown-body p").each(function(){
        lowercaseText = $(this).text().toLowerCase()
        if(lowercaseText.match("^"+"example") || lowercaseText.match("^"+"proof")){
            splited = $(this).html().split("<br>");
            extra = (splited[1] == null) ? "" : splited[1];
            $(this).html("<h3>"+note_number+"."+ counters[previous]+ ": "+ splited[0] +"</h3>"+"<p>"+extra+"</p>");
        }else{
            check($(this), 0);
        }
    });


    function check(instance, i){
        if(i>=needMatch.length)
            return;
        if(instance.text().toLowerCase().match("^"+needMatch[i])){
            counters[i]++;
            previous = i;
            splited = instance.html().split("<br>");
            extra = (splited[1] == null) ? "" : splited[1];
            instance.html("<"+tags[i]+">"+note_number+"."+ counters[i]+ ": "+ splited[0] +"</"+tags[i]+">"+"<p>"+extra+"</p>");
            return;
        }else
            check(instance,i+1);
    }
});