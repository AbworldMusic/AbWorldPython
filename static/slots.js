

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


$("th").on("click", function(){
    var filter = $(this).text().toLowerCase();

    backup = $("tr")
    $("tbody").empty();
    if(filter=="id"){
        ids = [];
        idElements = $(".id")
        for(i=0;i<idElements.length;i++){
            ids.push(idElements[i].innerHTML)
        }
        ids.sort();
        for(i=0;i<ids.length;i++){
            for(j=0;j<backup.length;j++){
                if(ids[i].toString()==$(backup[j]).find('.id').text()){
                    $("tbody").append($(backup[j]))
                }
            }
        }
    }
    if(filter=="name"){
        names = [];
        nameElements = $(".name")
        for(i=0;i<nameElements.length;i++){
            names.push($(nameElements[i]).find("a").text())
        }
        names.sort();
        for(i=0;i<names.length;i++){
            for(j=0;j<backup.length;j++){
                if(names[i].toString()==$(backup[j]).find('.name').text()){
                    $("tbody").append($(backup[j]))
                }
            }
        }
    }

})
