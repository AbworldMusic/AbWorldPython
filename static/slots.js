
$('select').select2();

$("#recurring-tab").click(function(){
    console.log("asd")
    $("#recurring").removeClass("d-none");
    $("#one-time").addClass("d-none");

    $("#recurring-tab").addClass("btn-primary")
    $("#recurring-tab").removeClass("btn-outline-primary")

    $("#one-time-tab").addClass("btn-outline-primary")
    $("#one-time-tab").removeClass("btn-primary")
})

$("#one-time-tab").click(function(){
    $("#one-time").removeClass("d-none");
    $("#recurring").addClass("d-none");

    $("#one-time-tab").addClass("btn-primary")
    $("#one-time-tab").removeClass("btn-outline-primary")

    $("#recurring-tab").removeClass("btn-primary")
    $("#recurring-tab").addClass("btn-outline-primary")

})

$('.hours').on('keyup', function(){
    console.log('hours')
   if(parseInt($(this).val())>12){
    $(this).val(12)
   }
   else if(parseInt($(this).val())<0){
    $(this).val(0)
   }
})
$('.minutes').on('keyup', function(){
   if(parseInt($(this).val())>59){
    $(this).val(59)
   }
   else if(parseInt($(this).val())<0){
    $(this).val(0)
   }
})

$('.submit').click(function(e){
    e.preventDefault();
    let hours = $(this).parents('form').find(".hours").val();
    let minutes = $(this).parents('form').find(".minutes").val();
    if(minutes==""){
        minutes="00"
    }
    if(hours==""){
        hours="00"
    }
    let ampm = $(this).parents('form').find(".ampm").children("option:selected").val();
    let time = hours +":"+ minutes +" "+ampm;
    $(this).parents('form').find(".time").val(time);
    $(this).parents('form').submit();

})

