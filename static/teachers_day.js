function OnComplete(){
    window.location.href="/teachers_day?completed=true"
}

function showLoader(){

    completed = 0;

    if($("#name").val().trim()!="" && $("#standard").val().trim()!="" && $("#top_angle_video").val().trim()!="" && $("#front_angle_video").val().trim()!=""){
        $(".submit-btn").prop("disabled", "true")
        $(".submit-btn").text("Uploading")
    }
    else{
       return true
    }
    var formData = new FormData();
    formData.append('name', $("#name").val().trim());
    formData.append('standard', $("#standard").val().trim());
    formData.append('branch', $("#branch").val().trim());

    var top_angle_chunks = [];
    var front_angle_chunks = [];
    var wish_chunks = [];

    var top_angle_progress = [];
    var front_angle_progress = [];
    var wish_progress = [];

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
            var chunkSize = 1024 * 1024;
            var fileSize = file.size;
            var chunks = Math.ceil(file.size/chunkSize,chunkSize);
            var chunk = 0;

            console.log('file size..',fileSize);
            console.log('chunks...',chunks);

            while (chunk <= chunks) {
                  var offset = chunk*chunkSize;
//                  console.log('current chunk..', chunk);
//                  console.log('offset...', chunk*chunkSize);
//                  console.log('file blob from offset...', offset)
//                  console.log(file.slice(offset,offset+chunkSize));
                  top_angle_chunks.push(chunk)

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
                            var index = top_angle_chunks.indexOf(parseInt(data));
                            top_angle_chunks.pop(index)
                            top_angle_progress.push(parseInt(data))



                            if (top_angle_progress.length==chunks){
                              completed = completed + 1;
                            }
                            if (completed == 2 && $("#wish_video")[0].files.length==0){
                              OnComplete();
                            } else if(completed == 3){
                              OnComplete();
                            }
                            $(".top-angle-progress").width("100%")
                           }
                           else{
                            $(".top-angle-progress").width(((top_angle_chunks.length/chunks)*100).toString()+"%")
                           }
                       }
                  });
                  chunk++;
            }

            var input = $("#front_angle_video")[0]
            var file = input.files[0]
            var chunkSize = 1024 * 1024;
            var fileSize = file.size;
            var chunks = Math.ceil(file.size/chunkSize,chunkSize);
            var chunk = 0;

            console.log('file size..',fileSize);
            console.log('chunks...',chunks);

            while (chunk <= chunks) {
                  var offset = chunk*chunkSize;
//                  console.log('current chunk..', chunk);
//                  console.log('offset...', chunk*chunkSize);
//                  console.log('file blob from offset...', offset)
//                  console.log(file.slice(offset,offset+chunkSize));

                  front_angle_chunks.push(chunk)
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
                            var index = front_angle_chunks.indexOf(parseInt(data));
                            front_angle_chunks.pop(index)
                            front_angle_progress.push(parseInt(data))

                            if (front_angle_progress.length==chunks){
                              completed = completed + 1;
                            }
                            if (completed == 2 && $("#wish_video")[0].files.length==0){
                              OnComplete();
                            } else if(completed == 3){
                              OnComplete();
                            }

                            $(".front-angle-progress").width("100%")
                           }
                           else{
                            $(".front-angle-progress").width(((front_angle_progress.length/chunks)*100).toString()+"%")
                           }

                       }
                  });
                  chunk++;
            }

            if($("#wish_video")[0].files.length>0){
                var input = $("#wish_video")[0]
            var file = input.files[0]
            var chunkSize = 1024 * 1024;
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

                  wish_chunks.push(chunk)

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
                            var index = wish_chunks.indexOf(parseInt(data));
                            wish_chunks.pop(index)
                            wish_progress.push(parseInt(data))

                            if (wish_progress.length==chunks){
                              completed = completed + 1;
                            }

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



