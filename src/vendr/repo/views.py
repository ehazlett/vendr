from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from repo.forms import UploadFileForm
import os
import uuid

def handle_upload(f, uuid):
    if not os.path.exists(settings.UPLOADS_DIR):
        os.makedirs(settings.UPLOADS_DIR)
    dest = open(os.path.join(settings.UPLOADS_DIR, uuid), 'wb+')
    for c in f.chunks():
        dest.write(c)
    dest.close()

def index(request):
    form = UploadFileForm(initial={'uuid': str(uuid.uuid4())})
    vars = RequestContext(request, {
        'form': form,
    })
    return render_to_response('index.html', vars)

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload(request.FILES['filename'], form.cleaned_data['uuid'])
    return HttpResponse('File: {0} uploaded...'.format(form.cleaned_data['uuid']))
