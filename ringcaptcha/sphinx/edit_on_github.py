import os
import warnings

def get_github_url(app, view, path):
    return 'https://github.com/{project}/{view}/{branch}/{path}'.format(
        project=app.config.edit_on_github_project,
        view=view,
        branch=app.config.edit_on_github_branch,
        path=path)

def html_page_context(app, pagename, templatename, context, doctree):
    if templatename != 'page.html':
        return

    if not app.config.edit_on_github_project:
        warnings.warn('edit_on_github_project not specified')
        return

    docroot = app.config.edit_on_github_docroot
    if docroot != '' and not docroot.endswith('/'):
        docroot += '/'

    path = docroot + os.path.relpath(doctree.get('source'), app.builder.srcdir)
    show_url = get_github_url(app, 'blob', path)
    edit_url = get_github_url(app, 'edit', path)

    context['show_on_github_url'] = show_url
    context['edit_on_github_url'] = edit_url

def setup(app):
    app.add_config_value('edit_on_github_project', '', True)
    app.add_config_value('edit_on_github_branch', 'master', True)
    app.add_config_value('edit_on_github_docroot', '', True)
    app.connect('html-page-context', html_page_context)
