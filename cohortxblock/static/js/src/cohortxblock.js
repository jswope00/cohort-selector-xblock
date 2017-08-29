/* Javascript for CohortXBlock. */
function CohortXBlock(runtime, element) {

    var handle_Url= runtime.handlerUrl(element, 'selected_value');

    $('#btn', element).click(function(eventObject) {
        selected_cohort = $("#student_cohort_list").val();    
        //selected_cohort_id = this.$('.cohort-select').val(); 
        console.log(selected_cohort);                   
        $.ajax({
        type: "POST",
        url: handle_Url,        
        data: JSON.stringify({selection:selected_cohort}), 
        success: location.reload()  
        });                                                                
      });    
}
