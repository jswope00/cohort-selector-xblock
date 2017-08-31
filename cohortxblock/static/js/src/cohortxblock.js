/* Javascript for CohortXBlock. */
function CohortXBlock(runtime, element) {

    var handle_Url= runtime.handlerUrl(element, 'selected_value');

    $('#btn', element).click(function(eventObject) {
        get_cohort_id();                                                       
      });

    function get_cohort_id(){
        var get_cohort_id_url = runtime.handlerUrl(element, 'get_cohort_id');
        selected_cohort = $("#student_cohort_list").val();    
        $.ajax({
          type: "POST",
          url: get_cohort_id_url,        
          data: JSON.stringify({selection:selected_cohort}), 
          success: add_user_to_cohort()  
        });       
    }

    function add_user_to_cohort(){
        var add_user_to_cohort_url = "http://54.84.102.234/courses/{{self.course_id}}/cohorts/{{self.selected_cohort_id}}/add"
        $.ajax({
        type: "POST",
        url: add_user_to_cohort_url,        
        data: {users:"{{user}}"}, 
        success: function (data) {
          console.log("Success : ");
          console.log(data);
          save_selected_cohort();
        },
        error: function (error) {
          console.log("Error");
          console.log(error);
        }  
    });  

    function save_selected_cohort(){
        var save_selected_cohort_url = runtime.handlerUrl(element, 'save_selected_cohort');
        selected_cohort = $("#student_cohort_list").val();
        $.ajax({
          type: "POST",
          url: save_selected_cohort_url,        
          data: JSON.stringify({selection:selected_cohort}), 
          success: function (data) {
            console.log("Success : ");
            console.log(data);
            location.reload();
          },
          error: function (error) {
            console.log("Error");
            console.log(error);
          }  
        });
    } 
  }    
}
