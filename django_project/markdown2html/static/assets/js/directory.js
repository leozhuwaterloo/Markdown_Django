// get all folders in our .directory-list
var nav_open = false;
$(document).ready(function(){
    var allFolders = $(".directory-list li > ul");
    allFolders.each(function() {
        // add the folder class to the parent <li>
        var folderAndName = $(this).parent();
        folderAndName.addClass("folder");

        // now add a slideToggle to the <a> we just added

    });

     $(".directory-toggle").click(function(e) {
        if(!$(this).siblings("ul").is(':animated')){
            $(this).siblings("ul").slideToggle("slow");
            e.preventDefault();
            $(this).toggleClass('minus');
        }
     });

    $("#menu-button").click(function() {
        if(!nav_open){
            $(".box").animate({
                "left": "0px",
            },{
                duration: 400,
                queue: false,
                complete: function(){nav_open=true;},
            });
        }else{
         $(".box").animate({
                "left": "-400px",
            },{
                duration: 400,
                queue: false,
                complete: function(){nav_open=false;},
            });
        }
        $("span[class^='mobile-menu']").toggleClass('toggle');
    });


    $(".markdown-body p").each(function(){
        $(this).html($(this).text().replace('\n','<br />'));
    });
});
