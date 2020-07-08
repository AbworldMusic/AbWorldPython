$('.level-btn').on("click", function(){
    id = $(this).attr('id');
    levelBtn = $(this)
    lessonsDiv = levelBtn.parents(".level").find(".lesson")
    if(lessonsDiv.hasClass("not-loaded")){
        $.ajax({
          type: 'POST',
          url: "/load_lessons",
          data: {"id": id},
          dataType: 'json',
          success: function(data){
            for(i=0;i<data.length;i++){
                let div = document.createElement("DIV")
                let link = document.createElement("A")
                link.href = "/view_lesson?id="+data[i]['id']
                link.innerHTML = data[i]['name']
                div.appendChild(link)
                $(div).addClass("p-2")
                $(div).addClass("bg-white border-bottom ")
                $(lessonsDiv).append(div)
            }
            lessonsDiv.removeClass("not-loaded")
            lessonsDiv.find("#loader").hide()
          }
        });
    }

})