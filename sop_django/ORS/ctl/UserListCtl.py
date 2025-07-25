from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from ..utility.HtmlUtility import HTMLUtility


class UserListCtl(BaseCtl):
    count = 1

    def preload(self, request, params):

        self.form["gender"] = request.POST.get('gender', '')

        if (params['id'] > 0):
            obj = self.get_service().get(params['id'])
            self.form["gender"] = obj.gender

        self.static_preload = {"Male": "Male", "Female": "Female"}

        self.form["preload"]["gender"] = HTMLUtility.get_list_from_dict(
            'gender',
            self.form["gender"],
            self.static_preload
        )


    def request_to_form(self, requestForm):
        self.form['firstName'] = requestForm.get("firstName", None)
        self.form['lastName'] = requestForm.get("lastName", None)
        self.form['login_id'] = requestForm.get("login_id", None)
        self.form['gender'] = requestForm.get("gender",None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        UserListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        UserListCtl.count += 1
        self.form['pageNo'] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        # self.form['LastId'] = User.objects.last().id
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        UserListCtl.count -= 1
        self.form['pageNo'] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = UserListCtl.count
        if (bool(self.form['ids']) == False):
            print("qqqqqaaaaaaaaaaaaaaaaaaaaaaaqqqq")
            self.form['error'] = True
            self.form['messege'] = "Please Select at least one Checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        else:
            print("qqqqqqqqqq-------------------------------")
            for ids in self.form['ids']:
                record = self.get_service().search(self.form)
                self.page_list = record['data']

                id = int(ids)
                if (id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        self.form['pageNo'] = 1
                        record = self.get_service().search(self.form)
                        self.page_list = record['data']
                        self.form['LastId'] = User.objects.last().id
                        UserListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        print("params---->>",params)
        UserListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "UserList.html"

    def get_service(self):
        return UserService()

