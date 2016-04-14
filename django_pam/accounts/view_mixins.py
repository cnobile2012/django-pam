# -*- coding: utf-8 -*-
#
# dcolumn/common/view_mixins.py
#

"""
Dynamic Column view mixins.
"""
__docformat__ = "restructuredtext en"

import logging, json
from django.http import HttpResponse

log = logging.getLogger('dcolumns.common.views')


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    response_class = HttpResponse

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.

        :param context: The template rendering context.
        :type context: See `Django Context <https://docs.djangoproject.com/en/dev/ref/templates/api/#playing-with-context-objects>`_.
        :param response_kwargs: Response keywords arguments.
        :rtype: See `Django response_class <https://docs.djangoproject.com/en/dev/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin.response_class>`_.
        """
        response_kwargs['content_type'] = 'application/json'
        return self.response_class(self.convert_context_to_json(context),
                                   **response_kwargs)

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object

        :param context: A dict of context data.
        :type context: dict
        :rtype: A JSON formatted string.
        """
        return json.dumps(context)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form. Must be used with an object-based
    FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Renders the context as JSON.

        :param context: A dict of context data.
        :type context: dict
        :rtype: See `Django's HttpResponse <https://docs.djangoproject.com/en/dev/ref/request-response/#httpresponse-objects>`_
        """
        data = json.dumps(context)
        #log.debug("data: %s", data)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        """
        Renders the invalid form error description. See `Django's form_invalid
        <https://docs.djangoproject.com/en/dev/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_invalid>`_.
        If the request is an AJAX request return this data as a JSON string.

        :param form: The Django form object.
        :type form: Django's form object.
        :rtype: Result from Django's ``form_valid`` or a JSON string.
        """
        response = super(AjaxableResponseMixin, self).form_invalid(form)

        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        """
        Renders the valid data. See `Django's form_valid <https://docs.djangoproject.com/en/dev/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_valid>`_.
        If the request is an AJAX request return this data as a JSON string.

        :param form: The Django form object.
        :type form: Django's form object.
        :rtype: Result from Django's ``form_valid`` or a JSON string.
        """
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)

        if self.request.is_ajax():
            data = {'pk': self.object.pk}
            return self.render_to_json_response(data)
        else:
            return response
