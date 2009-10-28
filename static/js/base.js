google.load("jquery", "1.2");
google.load("jqueryui", "1.5");

google.setOnLoadCallback(function() {
    
    $.fn.slugify = function(obj) {
        $(this).data('obj', jQuery(obj));
        $(this).keyup(function() {
            var obj = $(this).data('obj');
            var slug = $(this).val().replace(/\s+/g,'-').replace(/[^a-zA-Z0-9\-]/g,'').toLowerCase();
            obj.val(slug);
        });
    }

    $('#id_headline').slugify('#id_slug'); 
    $('#id_title').slugify('#id_title_slug');

});
