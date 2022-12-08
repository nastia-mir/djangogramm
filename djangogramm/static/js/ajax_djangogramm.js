$('.likeForm').on('submit', function(e) {
       e.preventDefault();

       var $this=$(this)
       var #button=$this.find('button[type="submit"]')

        $.ajax({
                url: ('.likeForm').data('url'),
                data: {},
                success:function(data){
                     $button.text();
                }
            })
        });



    })





})