from django.shortcuts import render
from ORS.ctl.BaseCtl import BaseCtl
from service.models import Favorite
from service.service.FavoriteService import FavoriteService


class FavoriteListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form['product'] = requestForm.get("product", None)
        self.form['addedDate'] = requestForm.get('addedDate', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        FavoriteListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params={}):
        FavoriteListCtl.count -= 1
        self.form['pageNo'] = FavoriteListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def next(self, request, params={}):
        FavoriteListCtl.count += 1
        self.form['pageNo'] = FavoriteListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def submit(self, request, params={}):
        FavoriteListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['mesg'] = "No record found"
        ress = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return ress

    def deleteRecord(self, request, params={}):
        self.form['pageNo'] = FavoriteListCtl.count
        if (bool(self.form['ids']) == False):
            self.form['error'] = True
            self.form['messege'] = "Please select at least one checkbox"
            record = self.get_service().search(self.form)
            self.page_list = record['data']
            res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        else:
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
                        self.form['LastId'] = Favorite.objects.last().id
                        FavoriteListCtl.count = 1

                        self.form['error'] = False
                        self.form['messege'] = "DATA HAS BEEN DELETED SUCCESSFULLY"
                        print('ppppppppp------->', self.page_list)
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
                    else:
                        self.form['error'] = True
                        self.form['messege'] = "DATA WAS NOT DELETED"
                        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "FavoriteList.html"

    def get_service(self):
        return FavoriteService()