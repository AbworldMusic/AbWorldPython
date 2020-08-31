function OnComplete(){
    window.location.href="/teachers_day?completed=true"
}

function uploadTopAngleVideo(link_id){
    let top_angle_chunks = [];
    let top_angle_progress = [];
    let input = $("#top_angle_video")[0]
    let file = input.files[0]
    let chunkSize = 1024 * 1024;
    let fileSize = file.size;
    let chunks = Math.ceil(file.size/chunkSize,chunkSize);
    let chunk = 0;

    console.log("Top angle video details")
    console.log('file size..',fileSize);
    console.log('chunks...',chunks);

    top_angle_loop = setInterval(function(){
        if(chunk >= chunks){
            clearInterval(top_angle_loop)
            uploadFrontAngleVideo();
        }
        let offset = chunk*chunkSize;
        top_angle_chunks.push(chunk)
        console.log("Uploading chunk number "+chunk.toString()+" for top angle")

        let formData = new FormData();
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
                    let index = top_angle_chunks.indexOf(parseInt(data));
                    top_angle_chunks.pop(index)
                    top_angle_progress.push(parseInt(data))

                    if (top_angle_progress.length==chunks){
                        completed = completed + 1;

                        if (completed == 2 && $("#wish_video")[0].files.length==0){
                          OnComplete();
                        } else if(completed == 3){
                          OnComplete();
                        }
                        $(".top-angle-progress").width("100%")
                   }
                   else{
                       $(".top-angle-progress").width(((top_angle_progress.length/chunks)*100).toString()+"%")
                   }
               }
              });
          chunk++;

    }, 700)

}

function uploadFrontAngleVideo(link_id){
    let front_angle_chunks = [];
    let front_angle_progress = [];
    let input = $("#front_angle_video")[0]
    let file = input.files[0]
    let chunkSize = 1024 * 1024;
    let fileSize = file.size;
    let chunks = Math.ceil(file.size/chunkSize,chunkSize);
    let chunk = 0;

    console.log("Front angle video details")
    console.log('file size..',fileSize);
    console.log('chunks...',chunks);

    front_angle_loop = setInterval(function(){
        if(chunk >= chunks){
            clearInterval(front_angle_loop)
            if($("#wish_video")[0].files.length>0){
                uploadWishVideo(link_id)
            }
            else{
                onComplete();
            }
        }
        let offset = chunk*chunkSize;
        front_angle_chunks.push(chunk)
        console.log("Uploading chunk number "+chunk.toString()+" for front angle")

        let formData = new FormData();
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
                    let index = front_angle_chunks.indexOf(parseInt(data));
                    front_angle_chunks.pop(index)
                    front_angle_progress.push(parseInt(data))

                    if (front_angle_progress.length==chunks){
                        completed = completed + 1;

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

    }, 700)

}

function uploadWishVideo(link_id){
    let wish_chunks = [];
    let wish_progress = [];

    let input = $("#wish_video")[0]
    let file = input.files[0]
    let chunkSize = 1024 * 1024;
    let fileSize = file.size;
    let chunks = Math.ceil(file.size/chunkSize,chunkSize);
    let chunk = 0;

    console.log('file size..',fileSize);
    console.log('chunks...',chunks);

    wish_loop = setInterval(function(){
    if(chunk >= chunks){
        clearInterval(wish_loop)
    }
    let offset = chunk*chunkSize;

    wish_chunks.push(chunk)

    let formData = new FormData();
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
            let index = wish_chunks.indexOf(parseInt(data));
            wish_chunks.pop(index)
            wish_progress.push(parseInt(data))

            if (wish_progress.length==chunks){
                completed = completed + 1;
                if (completed == 2 && $("#wish_video")[0].files.length==0){
                  OnComplete();
                } else if(completed == 3){
                  OnComplete();
                }
                $(".wish-progress").width("100%")
               }
               else{
                    $(".wish-progress").width(((wish_progress.length/chunks)*100).toString()+"%")
               }
            }
      });
      chunk++;
    }, 700);
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

    $.ajax({
        url: '/teachers_day_submission',
        type: 'POST',
        data : formData,
        processData: false,
        contentType: false,
        success: function(data){
            uploadTopAngleVideo(data);
        }

    });

    return false;
}



