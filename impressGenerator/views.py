from os import makedirs, remove
from shutil import copy, make_archive, rmtree

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect

from presentationTool.settings import DEBUG
from .models import *


def render_impress_content_to_string(request, the_presentation, release=False, last_focus_order_number=-1,
                                     focus_order_number=-1):
    try:
        last_focus_order_number = int(last_focus_order_number)
    except ValueError:
        last_focus_order_number = -1
    return render(request, 'impress.html',
                  {'presentation': the_presentation,
                   'release': release,
                   'last_focus_page_id': last_focus_order_number,
                   'focus_page_id': focus_order_number
                   }).content.decode()


def index(request):
    try:
        the_presentation = Presentation.objects.get(token=request.session['presentation-token'])
    except (KeyError, Presentation.DoesNotExist):
        the_presentation = Presentation.objects.create(name='')
        request.session['presentation-token'] = the_presentation.token
    return render(request, 'index.html', {'render_content': render_impress_content_to_string(request, the_presentation),
                                          'the_presentation': the_presentation})


def new_presentation(request):
    the_presentation = Presentation.objects.create(name='')
    request.session['presentation-token'] = the_presentation.token
    return redirect('index')


def add_page(request):
    the_presentation, _ = Presentation.objects.get_or_create(token=request.session['presentation-token'])
    the_presentation.name = request.POST['presentation-name']
    the_presentation.save()
    try:
        page_order_number = the_presentation.page_set.order_by('-page_order')[0].page_order + 1
    except IndexError:
        page_order_number = 1
    the_page = Page.objects.create(x=request.POST['x'] if request.POST['x'] != '' else 0,
                                   y=request.POST['y'] if request.POST['y'] != '' else 0,
                                   z=request.POST['z'] if request.POST['z'] != '' else 0,
                                   rx=request.POST['rx'] if request.POST['rx'] != '' else 0,
                                   ry=request.POST['ry'] if request.POST['ry'] != '' else 0,
                                   rz=request.POST['rz'] if request.POST['rz'] != '' else 0,
                                   scale=request.POST['scale'] if request.POST['scale'] != '' else 1,
                                   page_src=request.POST['content'],
                                   presentation=the_presentation,
                                   page_order=page_order_number)
    return JsonResponse({
        'page_content': render_impress_content_to_string(request, the_presentation,
                                                         last_focus_order_number=request.POST['last_page'][5:],
                                                         focus_order_number=the_page.page_order),
        'page_id': the_page.page_order,
        'page_summary': str(the_page)

    })


def remove_page(request):
    the_presentation, _ = Presentation.objects.get_or_create(token=request.session['presentation-token'])
    page_to_delete_order_number = request.POST['page-select']
    page_to_remove = the_presentation.page_set.get(page_order=page_to_delete_order_number)
    page_to_remove.delete()
    try:
        page_to_focus_order_number = the_presentation.page_set.order_by('-page_order')[0].page_order
    except IndexError:
        page_to_focus_order_number = -1
    return JsonResponse({
        'page_content': render_impress_content_to_string(request, the_presentation,
                                                         focus_order_number=page_to_focus_order_number)
    })


def set_page_info(the_page, x, y, z, rx, ry, rz, scale, content):
    the_page.x = x if x != '' else 0
    the_page.y = y if y != '' else 0
    the_page.z = z if z != '' else 0
    the_page.rx = rx if rx != '' else 0
    the_page.ry = ry if ry != '' else 0
    the_page.rz = rz if rz != '' else 0
    the_page.scale = scale if scale != '' else 1
    the_page.page_src = content
    the_page.save()


def edit_page(request):
    the_presentation, _ = Presentation.objects.get_or_create(token=request.session['presentation-token'])
    the_presentation.name = request.POST['presentation-name']
    the_presentation.save()
    the_page = the_presentation.page_set.get(page_order=request.POST['page-select'])
    set_page_info(the_page,
                  request.POST['x'], request.POST['y'], request.POST['z'],
                  request.POST['rx'], request.POST['ry'], request.POST['rz'],
                  request.POST['scale'], request.POST['content'])
    return JsonResponse({
        'page_content': render_impress_content_to_string(request, the_presentation,
                                                         last_focus_order_number=request.POST['last_page'][5:],
                                                         focus_order_number=the_page.page_order),
        'page_id': the_page.page_order,
        'page_summary': str(the_page)

    })


def download(request, presentation_id):
    if DEBUG:
        base_path = './'
    else:
        base_path = '/usr/src/app/'
    user_file_path = base_path + 'user-file/' + str(presentation_id)
    archive_path = base_path + 'user-archive/'
    the_presentation = Presentation.objects.get(id=presentation_id)
    web_page_src = render_impress_content_to_string(request, the_presentation, release=True)
    makedirs(user_file_path, exist_ok=True)
    makedirs(user_file_path + '/static/script', exist_ok=True)
    makedirs(user_file_path + '/static/stylesheet', exist_ok=True)
    makedirs(archive_path, exist_ok=True)
    with open(user_file_path + '/index.html', 'w') as file:
        file.write(web_page_src)
    copy(base_path + '/impressGenerator/static/script/impress.min.js',
         user_file_path + '/static/script/impress.min.js')
    copy(base_path + '/impressGenerator/static/stylesheet/impress_js_style.css',
         user_file_path + '/static/stylesheet/impress_js_style.css')
    make_archive(archive_path + str(the_presentation.id), 'zip',
                 user_file_path)
    response = FileResponse(open(archive_path + str(the_presentation.id) + '.zip', 'rb'))
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = 'attachment; filename=' + str(the_presentation.name) + '.zip'
    rmtree(user_file_path)
    remove(archive_path + str(the_presentation.id) + '.zip')
    return response
