from .models import AccessLogsModel
from django.conf import settings
from django.utils import timezone


class AccessLogsMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # create session
        if not request.session.session_key:
            request.session.create()

        access_logs_data = dict()

        # get the request path
        access_logs_data["request_path"] = request.path

        # get the client's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        access_logs_data["request_ip_address"] = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        access_logs_data["request_method"] = request.method
        access_logs_data["request_referrer"] = request.META.get('HTTP_REFERER',None)
        access_logs_data["session_key"] = request.session.session_key

        data = dict()
        data["get"] = dict(request.GET.copy())
        data['post'] = dict(request.POST.copy())

        # remove password form post data for security reasons
        keys_to_remove = ["password", "csrfmiddlewaretoken"]
        for key in keys_to_remove:
            data["post"].pop(key, None)

        access_logs_data["request_data"] = data
        access_logs_data["request_timestamp"] = timezone.now()

        response = self.get_response(request)

        # # save response
        access_logs_data["response_status"] = response.status_code
        access_logs_data["response_timestamp"] = timezone.now()
        access_logs_data["processed_time"] = str(access_logs_data["response_timestamp"] - access_logs_data["request_timestamp"])

        try:
            model = AccessLogsModel(**access_logs_data)
            model.save()
            # print log in console
            print(model)
        except Exception as e:
            pass

        return response
