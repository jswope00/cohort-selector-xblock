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
        success: add_user_to_cohort()  
        });                                                                
      });

      function add_user_to_cohort(){
        var add_user_to_cohort_url = "http://54.84.102.234/courses/{{self.course_id}}/cohorts/{{self.selected_cohort_id}}/add"
        $.ajax({
        type: "POST",
        url: add_user_to_cohort_url,        
        data: {users:"{{user}}"}, 
        success: function (data) {
                 console.log("Success : ");
                 console.log(data);
			         },
        error: function (error) {
                 console.log("Error");
                  console.log(error);
                                }  
        });   
      }    
}
