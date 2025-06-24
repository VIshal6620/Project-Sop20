from django.db import connection
from ORS.utility.DataValidator import DataValidator
from service.models import Customer
from service.service.BaseService import BaseService


class CustomerService(BaseService):

    def search(self, params):
        print('Page No -->', params['pageNo'])
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = 'select * from sos_Customer where 1=1'
        val = params.get('clientName', None)
        if (DataValidator.isNotNull(val)):
            sql += " and clientName like '" + val + "%%'"
        sql += " limit %s,%s"
        cursor = connection.cursor()
        print("------------>", sql, pageNo, self.pageSize)
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ('id', 'clientName', 'location', "contactNUmber", "importance")
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Customer
