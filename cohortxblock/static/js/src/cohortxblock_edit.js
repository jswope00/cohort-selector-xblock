/* Javascript for ZoomCloudRecordingEditBlock. */
function CohortXBlockEdit(runtime, element) {

  $(element).find('.save-button').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    var data = {
      general_title: $(element).find('input[name=general_title]').val(),
      instructions: $(element).find('input[name=instructions]').val(),
      cohort_display : $(element).find('select[id=cohort_list]').val(),
                                                                             
    };

    //console.log(data);
    
    runtime.notify('save', {state: 'start'});

    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      runtime.notify('save', {state: 'end'});
    });
  });

  $(element).find('.cancel-button').bind('click', function() {
    runtime.notify('cancel', {});
  });
}