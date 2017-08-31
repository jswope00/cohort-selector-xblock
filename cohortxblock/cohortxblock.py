"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader
from courseware import courses
from openedx.core.djangoapps.course_groups.cohorts import is_course_cohorted, get_course_cohorts, get_cohort_by_name, get_cohort_by_id, add_user_to_cohort
from django.contrib.auth.models import User
from opaque_keys.edx.locations import SlashSeparatedCourseKey

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

        context.update({
            "self": self
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
        user_email = User.objects.get(id=self.scope_ids.user_id)
        resp = self.add_users_to_cohort(user_email,self.course_id,verified_cohort.id)
        return resp

    @XBlock.json_handler                                
    def save_selected_cohort(self, data, suffix=''):
        self.selected_cohort = data.get('selection')
        return


    def add_users_to_cohort(self, user_email, course_key_string, cohort_id):
        """
        Return json dict of:

        {'success': True,
         'added': [{'username': ...,
                    'name': ...,
                    'email': ...}, ...],
         'changed': [{'username': ...,
                      'name': ...,
                      'email': ...,
                      'previous_cohort': ...}, ...],
         'present': [str1, str2, ...],    # already there
         'unknown': [str1, str2, ...]}

         Raises Http404 if the cohort cannot be found for the given course.
        """
        # this is a string when we get it here
        # course_key = SlashSeparatedCourseKey.from_deprecated_string(course_key_string)

        try:
            cohort = get_cohort_by_id(course_key_string, cohort_id)
        except CourseUserGroup.DoesNotExist:
            raise Http404("Cohort (ID {cohort_id}) not found for {course_key_string}".format(
                cohort_id=cohort_id,
                course_key_string=course_key_string
            ))

        users = user_email
        added = []
        changed = []
        present = []
        unknown = []
        for username_or_email in split_by_comma_and_whitespace(users):
            if not username_or_email:
                continue

            try:
                (user, previous_cohort) = add_user_to_cohort(cohort, username_or_email)
                info = {
                    'username': user.username,
                    'name': user.profile.name,
                    'email': user.email,
                }
                if previous_cohort:
                    info['previous_cohort'] = previous_cohort
                    changed.append(info)
                else:
                    added.append(info)
            except ValueError:
                present.append(username_or_email)
            except User.DoesNotExist:
                unknown.append(username_or_email)

        return json_http_response({'success': True,
                                   'added': added,
                                   'changed': changed,
                                   'present': present,
                                   'unknown': unknown})