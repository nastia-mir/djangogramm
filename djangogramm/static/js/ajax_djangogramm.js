$(document).ready( function() {

    $('.likeForm').submit( function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')
        const likes = parseInt($(this).attr("data-likes"))

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken':  window.CSRF_TOKEN,
                'post_id': post_id
            },
            success: function( data )
            {
                 $('.likeForm').hide();
                 $('.unlikeForm').show()
            }
         })
    });

$('.unlikeForm').submit(function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')
        const likes = parseInt($(this).attr("data-likes"))

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'post_id': post_id
            },
            success: function( data )
            {
                 $('.unlikeForm').hide();
                 $('.likeForm').show()
            }
         })
    });
})