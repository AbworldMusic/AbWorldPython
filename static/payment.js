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
          $(".month").html(data['month'])
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
    $(".fee-payment-tab").addClass('btn-primary')
    $(".instrument-sales-tab").removeClass('btn-primary')
    $(".fee-payment-tab").removeClass('btn-outline-primary')
    $(".instrument-sales-tab").addClass('btn-outline-primary')
    $('.fee-payment').removeClass("d-none");
    $(".instrument-sales").addClass('d-none');
})

$(".instrument-sales-tab").click(function(){
    $(".instrument-sales-tab").addClass('btn-primary')
    $(".fee-payment-tab").addClass('btn-primary')
    $(".instrument-sales-tab").removeClass('btn-outline-primary')
    $(".fee-payment-tab").addClass('btn-outline-primary')
    $('.instrument-sales').removeClass("d-none");
    $(".fee-payment").addClass('d-none');


})
