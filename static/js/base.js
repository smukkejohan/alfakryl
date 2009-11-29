google.load("jquery", "1.2");
google.load("jqueryui", "1.5");

google.setOnLoadCallback(function() {
    
    $('#articleslideshow').cycle({ 
        delay:  2000, 
        speed:  500, 
        before: onBefore 
    }); 
 
});
