from django.shortcuts import HttpResponse, render, redirect

from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        if request.path_info in ["/login/", "/image/code/"]:
            return

        info_dict = request.session.get("info")
        if info_dict:
            # if info_dict["id"] == 11:
            #     return redirect("/recommend/")
            return

        return redirect("/login/")
