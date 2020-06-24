

$('select').select2();

$('#datetimepicker1').datetimepicker({
    format: 'LT'
});
$('#datetimepicker2').datetimepicker({
    format: 'LT'
});
$('#datetimepicker3').datetimepicker({
    format: 'L'
});

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

