# This directory contains Jinja2 template files

This Flask application uses the Jinja2 templating engine to render data into HTML files.

The template files are organized into the following directories:

    common            # common base template files and macros
    flask_user        # flask_user template files (register, login, etc.)
    pages             # template files for web pages

flask_user makes use of standard template files that reside in  
`PATH/TO/VIRTUALENV/lib/PYTHONVERSION/site-packages/flask_user/templates/flask_user/`.  
These standard templates can be overruled by placing a copy in the `app/templates/flask_user/` directory.
