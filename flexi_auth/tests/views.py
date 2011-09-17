from django.http import HttpResponse

def normal_view(request):
    """
    A dummy 'regular' view
    """
    pass

class CallableView(object):
    """
    A dummy callable object to be used as a view
    """
    def __call__(self, *args, **kwargs):
        pass

def restricted_view(request):
    """
    Just a dummy view to test ``@object_permission_required`` decorator
    """
    return HttpResponse()
    