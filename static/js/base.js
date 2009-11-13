google.load("jquery", "1.2");
google.load("jqueryui", "1.5");

google.setOnLoadCallback(function() {  
    function onBefore() { 
        $('#phototitle')
            .html(this.alt); 
    };
});
