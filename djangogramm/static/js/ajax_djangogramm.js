$(document).ready( function() {

    $('.likeForm').submit( function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')

        let res;
        const likes_count = parseInt($(this).attr("data-likes"))

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
                 $('.likeForm').addClass("d-none");
                 $('.unlikeForm').removeClass("d-none");
                 likes = likes_count + 1
            }
         })
    });

    $('.unlikeForm').submit(function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')

        let res;
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
                 $('.unlikeForm').addClass("d-none");
                 $('.likeForm').removeClass("d-none");
                 res = likes - 1
            }
         })
    });

    $('.followForm').submit(function(e){
        e.preventDefault()
        const user_id = $(this).attr("data-uid");
        const url = $(this).attr('action')

        let res;
        const followers = parseInt($(this).attr("data-followers"))

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'user_id': user_id
            },
            success: function( data )
            {
                 $('.followForm').addClass("d-none");
                 $('.unfollowForm').removeClass("d-none");
                 res = followers - 1
            }
         })
    });

    $('.unfollowForm').submit(function(e){
        e.preventDefault()
        const user_id = $(this).attr("data-uid");
        const url = $(this).attr('action')

        let res;
        const followers = parseInt($(this).attr("data-followers"))

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'user_id': user_id
            },
            success: function( data )
            {
                 $('.unfollowForm').addClass("d-none");
                 $('.followForm').removeClass("d-none");
                 res = followers - 1
            }
         })
    });
})