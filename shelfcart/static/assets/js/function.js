console.log("function.js loaded!");
console.log("working fine");

const monthNames = ["Jan", "Feb", " Mar", "April", "May", "June", "July", "Aug",
    "Sept", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + ", " + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        datatype: "json",

        success: function(res){
            console.log("Comment Saved tp DB...");

            if(res.bool == true){
                $("#review-res").html("Review added successfully.")
               $(".hide-comment-form").hide()
                $(".add-review").hide()


                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                    _html += '<div class="user justify-content-between d-flex">'
                    _html += '<div class="thumb text-center">'
                    _html += '<img src="data:image/jpeg;base64,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" alt="" />'
                    _html += '<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>'
                    _html += '</div>'

                    _html += '<div class="desc">'
                    _html += '<div class="d-flex justify-content-between mb-10">'
                    _html += '<div class="d-flex align-items-center">'
                    _html += '<span class="font-xs text-muted">' + time +'</span>'
                    _html += '</div>'

                    for(let i = 1; i<=res.context.rating; i++){
                        _html += '<i class="fas fa-star text-warning"></i>';
                    }

                    _html += '</div>'
                    _html += '<p class="mb-10">'+ res.context.review +'</p>'

                    _html += '</div>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prep
                }
             
        }
    })
})


$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function(){
        console.log("A Checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;



        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val() 
            let filter_key = $(this).data("filter") //vendor, category

           console.log("Filter value is:", filter_value);
           console.log("Filter key is:", filter_key);     
            
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value;
            });
        });                                             
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend:function(){
                console.log("Trying to filter product...");
                
            },
            success:function(response){
                console.log(response);
                console.log("Data Filtered Successfully...");
                $("#filtered-product").html(response.data)
            }
        })  
    })

    $("#max_price").on("blur", function(){

        let min_price = parseFloat($(this).attr("min"))
        let max_price = parseFloat($(this).attr("max"))
        let current_price = parseFloat($(this).val())

        if(current_price < min_price || current_price > max_price){

            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert("Price must be between ₹" +min_price + " and ₹" +max_price)

            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()
            return false
        }
    });


    // --- Add to Cart functionality  ---    
    console.log("function.js loaded");

    $(".add-to-cart-btn").on("click", function () {
        console.log("Add to cart clicked!");

        const $btn = $(this);
        const index = $btn.attr("data-index");

        const product_id = $(".product-id-" + index).val();
        const product_title = $(".product-title-" + index).val();
        const quantity = parseInt($(".product-quantity-" + index).val() || 1);
        const product_price = $(".product-price-input-" + index).val();
        const product_pid = $(".product-pid-" + index).val();
        const product_image = $(".product-image-" + index).val();

        // hide old error
        $(`.stock-error-msg[data-error='${index}']`).hide();

        $.ajax({
            url: "/add-to-cart/",
            method: "GET",
            data: {
                'id': product_id,
                'title': product_title,
                'qty': quantity,
                'price': product_price,
                'pid': product_pid,
                'image': product_image
            },
            dataType: "json",

            success: function (response) {
                console.log("Added successfully!", response);
                $btn.html("✔");
                $(".cart-items-count").text(response.totalcartitems);
            },

            error: function (xhr) {
                let errorMsg = "Out of stock";

                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }

                $(`.stock-error-msg[data-error='${index}']`)
                    .text(errorMsg)
                    .show();
            }
        });
    });

    

    $(document).on("click", ".delete-product", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Product ID:", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data)
            }
        })
    })
    

    $(".update-product").on("click", function(){

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-"+product_id).val()

        console.log("Product ID:", product_id);
        console.log("Product qty:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "qty": product_quantity,
            },
            dataType:"json",
            beforeSend:function(){
                this_val.hide()
            },
            success:function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems);
                $("#cart-list").html(response.data)    
            }
        })

    })
    



    // Make Default Address Handler
    $(document).on('click', '.make-default-address', function () {
        let id = $(this).attr('data-address-id');
        let $button = $(this);  // the clicked button

        console.log("Clicked! Address ID:", id);

        $.ajax({
            url: '/make-default-address/',
            data: { 'id': id },
            dataType: 'json',
            success: function (response) {
                console.log("Success:", response);
                if (response.boolean === true) {
                    // Hide ALL checkmarks
                    $('.fa-check-circle').hide();

                    // Show ALL "Make default" buttons
                    $('.make-default-address').show();

                    // For the selected address: show checkmark and  hide button
                    $('.check' + id).show();        
                    $('.button' + id).hide();      
                }
            },
            error: function(xhr) {
                console.log("AJAX Error:", xhr.status, xhr.responseText);
            }
        });
    });   
    
    
    // Adding to wishlist
    $(document).on("click", ".add-to-wishlist", function(){
        let product_id = $(this).attr("data-product-item")
        let this_val = $(this)


        console.log("PRODUCT ID IS", product_id);



        $.ajax({
            url:"/add-to-wishlist",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Adding to wishlist...")
            },
            success: function(response){
                this_val.html("✔")
                if (response.bool === true){
                    console.log("Added to wishlist...");
                    $(".wishlist-count").text(response.wishlist_count);
                }
            }
        })
    })

    //Remove from wishlist
    $(document).on("click", ".delete-wishlist-product", function(){
        let wishlist_id = $(this).attr("data-wishlist-product")
        let this_val = $(this)

        console.log("wishlist id is:", wishlist_id);

        $.ajax({
            url: "/remove-from-wishlist",
            data: {
                "id":wishlist_id
            },
            dataType: "json",
            beforeSend: function(){
                console.log("Deleting product from wishlist...");
            },
            success: function(response){
                $("#wishlist-list").html(response.data)
                $(".wishlist-count").text(response.wishlist_count);
            }
        })
    })

    //contact us
    $(document).on("submit", "#contact-form-ajax", function(e){
        e.preventDefault()
        console.log("Submited...");

        let full_name = $("#full_name").val()
        let email = $("#email").val()
        let phone = $("#phone").val()
        let subject = $("#subject").val()
        let message = $("#message").val()


        console.log("Name:", full_name)
        console.log("email:", email)
        console.log("phone:", phone)
        console.log("subject:", subject)
        console.log("message:", message)

        $.ajax({
            url:"/ajax-contact-form",
            data:{
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "subject": subject,
                "message": message,
            },
            datatype:"json",
            beforeSend: function(){
                console.log("Sending Data to servere...");
            },
            success: function(res){
                console.log("Sent Data to servere!");
                $(".contact_us_p").hide()
                $("#contact-form-ajax").hide()
                $("#message-response").html("Message sent Successfully")
            }
        })
    })
 
})