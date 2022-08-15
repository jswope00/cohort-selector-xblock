"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from lms.djangoapps.courseware import courses
from openedx.core.djangoapps.course_groups.cohorts import get_course_cohorts, is_course_cohorted, get_cohort_by_name
from django.contrib.auth.models import User

loader = ResourceLoader(__name__)

class CohortXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    display_name = String(
        display_name="Cohort XBlock",
        help="This name appears in the horizontal navigation at the top of the page.",
        scope=Scope.settings,
        default="Cohort XBlock"
    )
    general_title = String(
        default="General Title", 
        scope=Scope.content, 
        help="General Title"
    )
    instructions = String(
        default="Instructions", 
        scope=Scope.content, 
        help="Paragraph text to show to students"
    )
    cohort_list= List(
        default=None, 
        scope=Scope.content, 
        help="List of cohorts"
    )
    cohort_display=List(
        default=None, 
        scope=Scope.content, 
        help="List of selected cohorts to be displayed"
    )
    selected_cohort=String(                                 
        default=None,
        scope=Scope.user_info,
        help="Specific user selection for cohort"
    )
    selected_cohort_id=String(
        default=None,
        scope=Scope.user_info,
        help="Selected cohort id"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the CohortXBlock, shown to students
        when viewing courses.
        """

        user = User.objects.get(id=self.scope_ids.user_id)

        context.update({
            "self": self,
	    "user":user
        })
        fragment = Fragment()
        fragment.add_content(loader.render_template("static/html/cohortxblock.html",context))
        fragment.add_javascript(loader.render_template("static/js/src/cohortxblock.js",context))
        fragment.add_css(self.resource_string("static/css/cohortxblock.css"))
        fragment.initialize_js('CohortXBlock')
        return fragment

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """

        if is_course_cohorted(self.course_id):
            course = courses.get_course(self.course_id)
            self.cohort_list = get_course_cohorts(course)


        context.update({
            "self": self
        })

        fragment = Fragment()
        fragment.add_content(loader.render_template("static/html/cohortxblock_edit.html",context))
        fragment.add_javascript(self.resource_string("static/js/src/cohortxblock_edit.js"))
        fragment.initialize_js('CohortXBlockEdit')
        return fragment

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.general_title = data.get('general_title')
        self.instructions = data.get('instructions')
        self.cohort_display = data.get('cohort_display')
        return {'result': 'success'}

    @XBlock.json_handler                                
    def get_cohort_id(self, data, suffix=''):
        verified_cohort = get_cohort_by_name(self.course_id, data.get('selection'))
        self.selected_cohort_id = str(verified_cohort.id)
        return verified_cohort.id

    @XBlock.json_handler                                
    def save_selected_cohort(self, data, suffix=''):
        self.selected_cohort = data.get('selection')
        return
