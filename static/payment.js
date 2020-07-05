$('select').select2();

$(".check-status").click(function(){
    let id = $("#student_id").val()
    if(id==""){
        alert("Please fill out ID")
        return false;
    }
    else{
    $(".loader").removeClass("d-none")

    $.ajax({
      type: 'POST',
      url: "/getStatus",
      data: {"id": id},
      dataType: 'json',
      success: function(data){
      console.log(data)
        if(data['name'].toString()=="No student found"){
          $(".no-student-found").removeClass("d-none")
          $(".details").addClass("d-none")

        }
        else{
          $(".no-student-found").addClass("d-none")
          $(".details").removeClass("d-none")
          $(".name").html(data['name'])
          $(".status").html(data['status'])
          $(".month").text(data['month'])
          $("#feeMonth").val(data['month'])
          if(data['status']=="Due"){
            $(".received").removeClass("d-none")
            $("#enrollment_id").val(id)
          }
        }
        $(".loader").addClass("d-none")
      }
    });
    }
})

$(".fee-payment-tab").click(function(){
    $(".instrument-sales-tab").addClass('btn-outline-primary')
    $(".instrument-sales-tab").removeClass('btn-primary')

    $(".other-sales-tab").addClass('btn-outline-primary')
    $(".other-sales-tab").removeClass('btn-primary')

    $(".fee-payment-tab").removeClass('btn-outline-primary')
    $(".fee-payment-tab").addClass('btn-primary')


    $(".instrument-sales").addClass('d-none');
    $('.other-sales').addClass("d-none");
    $('.fee-payment').removeClass("d-none");
})

$(".instrument-sales-tab").click(function(){
    $(".instrument-sales-tab").removeClass('btn-outline-primary')
    $(".instrument-sales-tab").addClass('btn-primary')

    $(".other-sales-tab").addClass('btn-outline-primary')
    $(".other-sales-tab").removeClass('btn-primary')


    $(".fee-payment-tab").addClass('btn-outline-primary')
    $(".fee-payment-tab").removeClass('btn-primary')

    $('.instrument-sales').removeClass("d-none");
    $('.other-sales').addClass("d-none");
    $(".fee-payment").addClass('d-none');


})

$(".other-sales-tab").click(function(){
    $(".other-sales-tab").removeClass('btn-outline-primary')
    $(".other-sales-tab").addClass('btn-primary')

    $(".instrument-sales-tab").addClass('btn-outline-primary')
    $(".instrument-sales-tab").removeClass('btn-primary')


    $(".fee-payment-tab").addClass('btn-outline-primary')
    $(".fee-payment-tab").removeClass('btn-primary')

    $('.instrument-sales').addClass("d-none");
    $('.other-sales').removeClass("d-none");
    $(".fee-payment").addClass('d-none');


})

$(".student-tab").on("change",function(){
    $("form .student-div").show()
    $("form .non-student-div").hide()
    $("form #student_id_input").prop('required',true);
    $("form #buyer_name").prop('required',false);
    $("form #buyer_email").prop('required',false);
    $("form #buyer_phone").prop('required',false);
    $("form #product_name").prop('required',false);
    $("form #product_price").prop('required',false);
})

$(".non-student-tab").on("change",function(){
    $(".non-student-div").show()
    $(".student-div").hide()
    $("form #student_id_input").prop('required',false);
    $("form #buyer_name").prop('required',true);
    $("form #buyer_email").prop('required',true);
    $("form #buyer_phone").prop('required',true);
    $("form #product_name").prop('required',false);
    $("form #product_price").prop('required',false);
})

$(".product-select").on("change", function(){
    if($(this).val().trim()=="Others"){
        $(".off-inventory-item").show();
        $("form #product_name").prop('required',true);
        $("form #product_price").prop('required',true);
    }
    else{
        $(".off-inventory-item").hide();
        $("form #product_name").prop('required',false);
        $("form #product_price").prop('required',false);
    }
})
