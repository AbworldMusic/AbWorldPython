

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
    if(filter=="id"){
        ids = [];
        idElements = $(".id")
        for(i=0;i<idElements.length;i++){
            ids.push(parseInt(idElements[i].innerHTML))
        }
        ids.sort(function(a, b){return a-b});
        $("tbody").empty();

        for(i=0;i<ids.length;i++){
            for(j=0;j<backup.length;j++){
                if(ids[i].toString().trim()==$(backup[j]).find('.id').text().trim()){
                    $("tbody").append($(backup[j]))
                }
            }
        }
    }
    if(filter=="name"){
        names = [];
        nameElements = $(".name")
        for(i=0;i<nameElements.length;i++){
            names.push($(nameElements[i]).text().trim())
        }
        names.sort();
        $("tbody").empty();

        for(i=0;i<names.length;i++){
            for(j=0;j<backup.length;j++){
                if(names[i].toString().trim()==$(backup[j]).find('.name').text().trim()){
                    $("tbody").append($(backup[j]))
                }
            }
        }
    }

})
