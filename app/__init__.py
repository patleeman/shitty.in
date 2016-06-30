from flask import Flask


# Need to change Flask Jinja 2 delimiters so app.js works without modification.
# https://gist.github.com/lost-theory/3925738
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='%%',
        variable_end_string='%%',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = CustomFlask(__name__)
from app import views

