$('#datetimepicker3').datetimepicker({
    format: 'L'
});

$("#getAnotherDay").on("click", function(){
   let newDate = $("#newDate").val();
   if(newDate.trim()!='')
   window.location.href = "dailyTransactions?on="+newDate

})