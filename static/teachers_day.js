function OnComplete(){
    window.location.href="/teachers_day?completed=true"
}

function showLoader(){
    completed = 0;

    if($("#name").val().trim()!="" && $("#standard").val().trim()!="" && $("#top_angle_video").val().trim()!="" && $("#front_angle_video").val().trim()!=""){
        console.log("All inputs received")
    }
    else{
       return true
    }
    var formData = new FormData();
    formData.append('name', $("#name").val().trim());
    formData.append('standard', $("#standard").val().trim());
    formData.append('branch', $("#branch").val().trim());

    $.ajax({
        url: '/teachers_day_submission',
        type: 'POST',
        data : formData,
        processData: false,
        contentType: false,
        success: function(data){
            var link_id = data
            var input = $("#top_angle_video")[0]
            var file = input.files[0]
            var chunkSize = 1024 * 1024 * 5;
            var fileSize = file.size;
            var chunks = Math.ceil(file.size/chunkSize,chunkSize);
            var chunk = 0;

            console.log('file size..',fileSize);
            console.log('chunks...',chunks);

            while (chunk <= chunks) {
                  var offset = chunk*chunkSize;
                  console.log('current chunk..', chunk);
                  console.log('offset...', chunk*chunkSize);
                  console.log('file blob from offset...', offset)
                  console.log(file.slice(offset,offset+chunkSize));



                  var formData = new FormData();
                  formData.append('file', file.slice(offset,offset+chunkSize));
                  formData.append('chunk_number', chunk);
                  formData.append('total_chunks', chunks);
                  formData.append('file_name', file.name);
                  formData.append('link_id', link_id);
                  formData.append('file_type', "top_angle_video");
                  formData.append('byteoffset', offset);
                  $.ajax({
                       url : '/teachers_day_upload',
                       type : 'POST',
                       data : formData,
                       processData: false,
                       contentType: false,
                       success : function(data) {
                           if (data=="Complete"){
                            completed = completed + 1;
                            if (completed == 2 && $("#wish_video")[0].files.length==0){
                              OnComplete();
                            } else if(completed == 3){
                              OnComplete();
                            }
                            $(".top-angle-progress").width("100%")
                           }
                           else{
                            $(".top-angle-progress").width(((parseFloat(data)/chunks)*100).toString()+"%")
                           }
                       }
                  });
                  chunk++;
            }

            var input = $("#front_angle_video")[0]
            var file = input.files[0]
            var chunkSize = 1024 * 1024 * 5;
            var fileSize = file.size;
            var chunks = Math.ceil(file.size/chunkSize,chunkSize);
            var chunk = 0;

            console.log('file size..',fileSize);
            console.log('chunks...',chunks);

            while (chunk <= chunks) {
                  var offset = chunk*chunkSize;
                  console.log('current chunk..', chunk);
                  console.log('offset...', chunk*chunkSize);
                  console.log('file blob from offset...', offset)
                  console.log(file.slice(offset,offset+chunkSize));

                  var formData = new FormData();
                  formData.append('file', file.slice(offset,offset+chunkSize));
                  formData.append('chunk_number', chunk);
                  formData.append('total_chunks', chunks);
                  formData.append('file_name', file.name);
                  formData.append('link_id', link_id);
                  formData.append('file_type', "front_angle_video");
                  formData.append('byteoffset', offset);
                  $.ajax({
                       url : '/teachers_day_upload',
                       type : 'POST',
                       data : formData,
                       processData: false,
                       contentType: false,
                       success : function(data) {
                           if (data=="Complete"){
                            completed = completed + 1;
                            if (completed == 2 && $("#wish_video")[0].files.length==0){
                              OnComplete();
                            } else if(completed == 3){
                              OnComplete();
                            }

                            $(".front-angle-progress").width("100%")
                           }
                           else{
                            $(".front-angle-progress").width(((parseFloat(data)/chunks)*100).toString()+"%")
                           }

                       }
                  });
                  chunk++;
            }

            if($("#wish_video")[0].files.length>0){
                var input = $("#wish_video")[0]
            var file = input.files[0]
            var chunkSize = 1024 * 1024 * 5;
            var fileSize = file.size;
            var chunks = Math.ceil(file.size/chunkSize,chunkSize);
            var chunk = 0;

            console.log('file size..',fileSize);
            console.log('chunks...',chunks);

            while (chunk <= chunks) {
                  var offset = chunk*chunkSize;
                  console.log('current chunk..', chunk);
                  console.log('offset...', chunk*chunkSize);
                  console.log('file blob from offset...', offset)
                  console.log(file.slice(offset,offset+chunkSize));

                  var formData = new FormData();
                  formData.append('file', file.slice(offset,offset+chunkSize));
                  formData.append('chunk_number', chunk);
                  formData.append('total_chunks', chunks);
                  formData.append('link_id', link_id);
                  formData.append('file_name', file.name);
                  formData.append('file_type', "wish_video");
                  formData.append('byteoffset', offset);
                  $.ajax({
                       url : '/teachers_day_upload',
                       type : 'POST',
                       data : formData,
                       processData: false,
                       contentType: false,
                       success : function(data) {
                           if (data=="Complete"){
                           completed = completed + 1;
                            if (completed == 2 && $("#wish_video")[0].files.length==0){
                              OnComplete();
                            } else if(completed == 3){
                              OnComplete();
                            }
                            $(".wish-progress").width("100%")
                           }
                           else{
                            $(".wish-progress").width(((parseFloat(data)/chunks)*100).toString()+"%")
                           }
                       }
                  });
                  chunk++;
            }

            }
        }

    });

    return false;
}



