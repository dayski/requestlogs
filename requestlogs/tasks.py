import datetime

from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404

from celery import task

from . import request_log
from .settings import REQUEST_META_KEYS


def find(*args, **kwargs):
    """
    kwargs supported:
        user: the username
        start_at: start datetime object
        end_at: end datetime object
        limit: # of objects to fetch
    """
    # default end_at to now and start to 1 day from now
    end_at = kwargs.get('end_at', datetime.datetime.now())
    start_at = kwargs.get('start_at', end_at - datetime.timedelta(days=1))

    # default # of records to fetch to be 50
    limit = kwargs.get('limit', 50)

    # if no user is defined, fetch for ALL
    user = kwargs.get('user', None)
    if user:
        return request_log.find(start_at, end_at, limit, spec={'user': user})
    else:
        return request_log.find(start_at, end_at, limit)


@task
def write_to_db(request, response_code, start_at, end_at):
    # extract specific data from the META KEYS
    r_meta = dict()
    for i in REQUEST_META_KEYS:
        r_meta[i] = request.META.get(i, None)

    # extract the view details, args & kwargs
    try:
        myfunc, myargs, mykwargs = resolve(request.path_info)

        # for piston - use handler to extract view / class information
        if module == 'piston.resource':
            pfunc = myfunc.handler
            view = '%s.%s' % (pfunc.__module__, pfunc.__class__.__name__)
        else:
            view = '%s.%s' % (myfunc.__module__, myfunc.__name__)

    except Resolver404, Http404:
        # unable to find the details, set blanks
        view = None
        myargs = ()
        mykwargs = {}

    # let's prepare the dict!
    log_dict = {
        'url': request.get_full_path(),  # the url
        'view': view,                    # view name, for perf checks
        'args': list(myargs),            # args & kwargs
        'kwargs': mykwargs,
        'get': request.GET,              # GET & POST data - raw
        'post': request.POST,
        'meta': r_meta,                  # meta keys
        'status': response_code,         # response status
        'user': request.user.username,   # logged in user
        't': end_at - start_at,          # time to serve the request
    }

    request_log.save(log_dict)
