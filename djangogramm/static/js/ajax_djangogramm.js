$(document).ready( function() {

    $('.likeForm').submit( function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')

        var likes = parseInt($('span').html())

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken':  window.CSRF_TOKEN,
                'post_id': post_id
            },
            success: function(data)
            {
                 $('.likeForm').addClass("d-none");
                 $('.unlikeForm').removeClass("d-none");
                 $('.likeCount').text(likes + 1)
            }
         })
    });

    $('.unlikeForm').submit(function(e){
        e.preventDefault()
        const post_id = $(this).attr("data-postId");
        const url = $(this).attr('action')

        var likes = parseInt(parseInt($('span').html()))

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'post_id': post_id
            },
            success: function(data)
            {
                 $('.unlikeForm').addClass("d-none");
                 $('.likeForm').removeClass("d-none");
                 $('.likeCount').text(likes - 1)
            }
         })
    });

    $('.followForm').submit(function(e){
        e.preventDefault()
        const user_id = $(this).attr("data-uid");
        const url = $(this).attr('action')

        var followers = parseInt($('span').html())

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'user_id': user_id
            },
            success: function(data)
            {
                 $('.followForm').addClass("d-none");
                 $('.unfollowForm').removeClass("d-none");
                 $('.followerCount').text(followers + 1)
            }
         })
    });

    $('.unfollowForm').submit(function(e){
        e.preventDefault()
        const user_id = $(this).attr("data-uid");
        const url = $(this).attr('action')

        var followers = parseInt($('span').html())

        $.ajax(
        {
            type:"POST",
            url: url,
            data:{
                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                'user_id': user_id
            },
            success: function(data)
            {
                 $('.unfollowForm').addClass("d-none");
                 $('.followForm').removeClass("d-none");
                 $('.followerCount').text(followers - 1)
            }
         })
    });
})