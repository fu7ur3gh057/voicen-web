import json

from rest_framework.renderers import JSONRenderer


class WalletJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_types=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(WalletJSONRenderer, self).render(data)
        return json.dumps({"wallet": data})


# class OperationJSONRenderer(JSONRenderer):
#     charset = 'utf-8'
#
#     def render(self, data, accepted_media_types=None, renderer_context=None):
#         errors = data.get('errors', None)
#
#         if errors is not None:
#             return super(OperationJSONRenderer, self).render(data)
#         return json.dumps({"email": data['email'], "operation_list": data})
