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



})