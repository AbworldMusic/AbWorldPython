$(document).ready(function(){

    $('.hobby').click(function(){
        $('#hobby-fee').show();
        $('#intermediate-fee').hide();
        $('#advanced-fee').hide();
        $('#batch').select2({
            maximumSelectionLength: 2
        });
        $('#batch').css('width', '100%')
    })
    $('.intermediate').click(function(){
        $('#hobby-fee').hide();
        $('#intermediate-fee').show();
        $('#advanced-fee').hide();
        $('#batch').select2({
            maximumSelectionLength: 3
        });
        $('#batch').css('width', '100%')

    })
    $('.advanced').click(function(){
        $('#hobby-fee').hide();
        $('#intermediate-fee').hide();
        $('#advanced-fee').show();
        $('#batch').select2({
            maximumSelectionLength: 4
        });
        $('#batch').css('width', '100%')
    })

    $('select').select2();
    $('#batch').select2({
        maximumSelectionLength: 2
    });

    $(".next_btn").on("click", function(){
        var currentIndex = $('div.active').index() + 1;
        if(currentIndex==1){
            if($("input#studentName").val().trim()==""){
                $("input#studentName").focus();
                return false;
            }
            else if($("#male_gender").prop("checked")== false && $("#female_gender").prop("checked")==false){
                alert("Gender cannot be empty");
                $("#male_gender").focus();
                return false;
            }
            else if($("input#studentAge").val().trim()==""){
                $("input#studentAge").focus();
                return false;
            }
            else if($("input#studentDob").val().trim()==""){
                $("input#studentDob").focus();
                return false;
            }
            else if($("input#address").val().trim()==""){
                $("input#address").focus();
                return false;
            }
            if($("#enrollment_type").val()=="True"){

                if($("input#fatherName").val().trim()==""){
                    $("input#fatherName").focus();
                    return false;
                }
                else if($("input#fatherPhone").val().trim()==""){
                    $("input#fatherPhone").focus();
                    return false;
                }
                else if($("input#fatherEmail").val().trim()==""){
                    $("input#fatherEmail").focus();
                    return false;
                }
                else if($("input#fatheroccupation").val().trim()==""){
                    $("input#fatheroccupation").focus();
                    return false;
                }
                else if($("input#motherName").val().trim()==""){
                    $("input#motherName").focus();
                    return false;
                }
                else if($("input#motherPhone").val().trim()==""){
                    $("input#motherPhone").focus();
                    return false;
                }
                else if($("input#motherEmail").val().trim()==""){
                    $("input#motherEmail").focus();
                    return false;
                }
                else if($("input#motheroccupation").val().trim()==""){
                    $("input#motheroccupation").focus();
                    return false;
                }
                else{
                    $('.carousel').carousel('next')
                }
            }
            else{
                if($("input#phone").val().trim()==""){
                    $("input#phone").focus();
                    return false;
                }
                else if($("input#email").val().trim()==""){
                    $("input#email").focus();
                    return false;
                }
                else{
                    $('.carousel').carousel('next')
                }
            }
        }
        else if(currentIndex==2){
            if($("#guitar").prop("checked")== false && $("#keyboard").prop("checked")==false && $("#drums").prop("checked")==false){
                alert("Selecting an instrument is mandatory")
                return false;
            }
            else if($("#haveInstrumentYes").prop("checked")== false && $("#haveInstrumentNo").prop("checked")==false){
                alert("Please enter if student has instrument")
                return false;
            }
            else if($("#hobby").prop("checked")== false && $("#intermediate").prop("checked")==false && $("#advanced").prop("checked")==false){
                alert("Please select a batch")
                return false;
            }
            else if($("#hobby").prop("checked")==true &&  $("#batch :selected").length<2){
                alert("You need to select a minimum of 2 slots");
                return false;
            }
            else if($("#intermediate").prop("checked")==true &&  $("#batch :selected").length<3){
                alert("You need to select a minimum of 3 slots");
                return false;
            }
            else if($("#advanced").prop("checked")==true &&  $("#batch :selected").length<4){
                alert("You need to select a minimum of 4 slots");
                return false;
            }
            else if($("input#joiningDate").val().trim()==""){
                $("input#joiningDate").focus();
                return false;
            }
            else{
                $('.carousel').carousel('next')
            }
        }
    })



})