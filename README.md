# Cohort Selector X-block
An embeddable xblock that will simply allow a user to self-select their cohort in a course.  

Installation
------------

Make sure that `ALLOW_ALL_ADVANCED_COMPONENTS` feature flag is set to `True` in `cms.env.json`.

Change user and activate env:

```bash
sudo -H -u edxapp bash
source /edx/app/edxapp/edxapp_env
```

Get the source to the /edx/app/edxapp/ folder:

```bash
cd /edx/app/edxapp/
git clone https://github.com/jswope00/cohort-selector-xblock.git
```

For Installation:
```bash
pip install cohort-selector-xblock/
```

To upgrade an existing installation of this XBlock, fetch the latest code and then update:

```bash
cd cohort-selector-xblock/
git pull origin master
cd ..
pip install -U --no-deps cohort-selector-xblock/
```

Configuration
-------------

Go to ```edx-platform/openedx/core/djangoapps/course_groups/views.py:```

Find the function ```def add_users_to_cohort(request, course_key_string, cohort_id):```

Under the function, perform the following change:

```bash
get_course_with_access(request.user, 'staff', course_key)
```
Replace 'staff' with 'load'

```bash
get_course_with_access(request.user, 'load', course_key)
```

Restart Edxapp:

```bash
exit
sudo /edx/bin/supervisorctl restart edxapp:
```

Enabling in Studio
------------------

You can enable the cohort-selector-xblock in studio through the advanced
settings.

1. From the main page of a specific course, navigate to `Settings ->
   Advanced Settings` from the top menu.
2. Check for the `advanced_modules` policy key, and add
   `"cohortxblock"` to the policy value list.
3. Click the "Save changes" button.
