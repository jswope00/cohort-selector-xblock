# Cohort Selector X-block
An embeddable xblock that will simply allow a user to self-select their cohort in a course.  

Installation
------------

Access the LMS/CMS docker container:
```bash
docker exec -it tutor_local_lms_1 /bin/bash    # For LMS
docker exec -it tutor_local_cms_1 /bin/bash    # For CMS
```

Clone the Cohort Selector repository here:
```bash
git clone https://github.com/jswope00/cohort-selector-xblock.git
```

Access the Cohort Selector directory:
```bash
cd cohort-selector-xblock/
```

Install this using the following command:
```bash
pip install -e .
```

To upgrade an existing installation of this XBlock, fetch the latest code and then update:
```bash
git pull origin master
cd ..
pip install -U --no-deps cohort-selector-xblock/
```

Configuration
-------------

Access the ```edx-platform/openedx/core/djangoapps/course_groups/views.py``` file.

Find the function ```def add_users_to_cohort(request, course_key_string, cohort_id)```:

Under the function, perform the following change:

```bash
get_course_with_access(request.user, 'staff', course_key)
```
Replace 'staff' with 'load'

```bash
get_course_with_access(request.user, 'load', course_key)
```

Restart the Server:
```bash
tutor local restart
```

Note: Installation and Configuration steps are to be done for LMS and CMS both.

Enabling in Studio
------------------

You can enable the cohort-selector-xblock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add
   `"cohortxblock"` to the policy value list.
3. Click the "Save changes" button.
