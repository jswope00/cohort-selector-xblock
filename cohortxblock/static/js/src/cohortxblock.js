/* Javascript for CohortXBlock. */
function CohortXBlock(runtime, element) {

    var handle_Url= runtime.handlerUrl(element, 'selected_value');

    $('#btn', element).click(function(eventObject) {
        get_cohort_id();                                                       
	$('#notification_messages').empty();
	$('#error_messages').empty();
      });

    function get_cohort_id(){
        var get_cohort_id_url = runtime.handlerUrl(element, 'get_cohort_id');
        selected_cohort = $("#student_cohort_list").val();    
        $.ajax({
          type: "POST",
          url: get_cohort_id_url,        
          data: JSON.stringify({selection:selected_cohort}), 
          success: function (data) {
            console.log("Success : ");
            console.log(data);
            generate_message(data);
          },
          error: function (error) {
            console.log("Error");
            console.log(error);
          }
        });       
    }
 
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
          },
          error: function (error) {
            console.log("Error");
            console.log(error);
          }  
        });
    }

    function generate_message(modifiedUsers){
        var numUsersAdded, numPresent, message
        numUsersAdded = modifiedUsers.added.length + modifiedUsers.changed.length;
        message = ""
        error = ""
        if (numUsersAdded > 0) {
          message = "Your preferences have been saved."
          message += "<br>You have been added to this cohort."
          save_selected_cohort();
        }
        numChanged = modifiedUsers.changed.length;
        if (numChanged > 0) {
          message += "<br>You have been removed from "+modifiedUsers.changed[0].previous_cohort
        }
        numPresent = modifiedUsers.present.length;
        if (numPresent > 0){
          message = "You are already in this cohort"
        }
        numErrors = modifiedUsers.unknown.length;
        if (numErrors >0){
          error = "You could not be added to this cohort"
        }
        $('#notification_messages').append(message);
        $('#error_messages').append(error);
    } 
  }