from django.forms.models import model_to_dict
from django.shortcuts import render
from .models import Theme

import json

try:
    from kharon import kharon
    kharon_avail = True
except Exception:
    kharon_avail = False

# from django.http import HttpResponse


def themes_view(request, **kwargs):
    return _render(request, 'themes.html')


def about_view(request, **kwargs):
    return _render(request, 'about.html')


def cookies_view(request, **kwargs):
    return _render(request, 'cookies.html')


def home_view(request, **kwargs):
    return _render(request, 'home.html')


def wip_view(request, **kwargs):
    return _render(request, 'wip.html')


def gaming_view(request, **kwargs):
    return _render(request, 'gaming.html')


def music_view(request, **kwargs):
    return _render(request, 'music.html')


def contact_view(request, **kwargs):
    return _render(request, 'contact.html')


def coding_view(request, **kwargs):
    return _render(request, 'coding.html')


def wd2_view(request, **kwargs):
    return _render(request, 'wd2.html')


def landing_view(request, **kwargs):
    if 'landed' in request.COOKIES or request.user_agent.is_touch_capable:
        response = home_view(request, **kwargs)
    elif not request.user_agent.is_touch_capable:
        response = wd2_view(request, **kwargs)
        response.set_cookie('landed', '1')
    return response


def submit_view(request, **kwargs):
    return _render(request, 'submit.html')


def _render(request, target, **kwargs):

    age = 60 * 60 * 24 * 7

    primary = request.GET.get('primary')
    secondary = request.GET.get('secondary')
    theme = request.GET.get('theme_name')

    try:
        theme_model = Theme.objects.get(key=theme)
    except Exception:
        theme_model = None

    if not (primary and secondary):
        if theme_model:
            primary = theme_model.primary
            secondary = theme_model.secondary
        elif 'primary' in request.COOKIES and 'secondary' in request.COOKIES:
            primary = request.COOKIES['primary']
            secondary = request.COOKIES['secondary']
        else:
            primary = 'aqua'
            secondary = 'purple'

    kwargs['gk_theme_primary'] = primary
    kwargs['gk_theme_secondary'] = secondary
    kwargs['gk_theme_data'] = [
        model_to_dict(model) for model in Theme.objects.all()]

    response = render(request, target, kwargs)
    response.set_cookie('primary', primary, max_age=age)
    response.set_cookie('secondary', secondary, max_age=age)
    return response


def kharon_controller(request, **kwargs):
    preview = ''
    output = ''
    target = 'content'

    username = request.GET.get('username_text') or 'gannon93'
    reponame = request.GET.get('reponame_text') or 'gkit_cogs'
    cogname = request.GET.get('cogname_text') or 'basta'

    if request.GET.get('upload_github_button'):
        if kharon_avail:
            try:
                preview = json.dumps(
                    kharon.get_info(
                        username.lower(), reponame.lower(), cogname.lower()),
                    sort_keys=True)
                target = 'convert'
            except Exception as e:
                pass
    elif request.GET.get('convert_button'):
        data = request.GET.get('upload_preview_textarea')
        preview = json.loads(data)
        if kharon_avail:
            output = kharon.format_info(preview)
        target = 'export'

    kwargs = {
        'preview': preview,
        'output': output,
        'username': username,
        'reponame': reponame,
        'cogname': cogname,
        'gotodiv': target}
    return kwargs


def kharon_view(request, **kwargs):
    kwargs = kharon_controller(request, **kwargs)
    return _render(
        request, 'kharon.html', **kwargs)
