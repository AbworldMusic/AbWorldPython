$(document).ready(function(){
    id = $("#lesson_id").text()
    $.ajax({
        type: 'POST',
        url: "/view_images_for_lesson",
        data: {"id": id},
        dataType: 'json',
        success: function(data){
            imagesDiv = $(".images")
            for(i=0;i<data.length;i++){
                div = document.createElement("DIV")
                $(div).addClass('col-6')
                img = document.createElement("IMG")
                img.src = "MySite/images/"+data[i]
                div.appendChild(img)
                imagesDiv.append($(div))
            }
        }
    });
})