#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from   config   import *

from   datetime import *
from   time     import *
import requests
import re

################################################################################################
class PeeringDB():
    def __init__(self):
        self.str_url    = "https://peeringdb.com/api"
        self.dic_header = {"Accept":"application/json"}

    def get(self,str_url,str_filter=None):
        response  = requests.get(str_url, headers=self.dic_header)
        if str_filter == None:
            return response.json()
        else:
            json_data  = {"data":[]}
            for dic_tmp in response.json()["data"]:
                if re.findall(str_filter,dic_tmp["name"]):
                    json_data["data"].append(dic_tmp)
            return self.gen_db2json(json_data)

    def gen_db2json(self,json_data):
        json_data = {"data":json_data["data"],"meta":{"generated":mktime(datetime.now().timetuple())}}
        return json_data

    def get_IXinfo(self,str_filter=None):
        str_endpoint = "/ix"
        if str_filter == None:
            return self.get(self.str_url+str_endpoint)
        else:
            return self.get(self.str_url+str_endpoint,str_filter)

    def gen_IXid(self,str_filter=None):
        dic_ixdata   = {}
        str_endpoint = "/ix"
        if str_filter == None:
            json_ix = self.get(self.str_url+str_endpoint)
            for dic_tmp in json_ix["data"]:
                dic_ixdata.update({dic_tmp["id"]:dic_tmp["name"]})
            return dic_ixdata
        else:
            json_ix = self.get(self.str_url+str_endpoint,str_filter)
            for dic_tmp in json_ix["data"]:
                if re.findall(str_filter,dic_tmp["name"]):
                    dic_ixdata.update({dic_tmp["id"]:dic_tmp["name"]})
            return dic_ixdata

    def get_NETinfo(self,str_filter=None):
        str_endpoint = "/net"
        if str_filter == None:
            return self.get(self.str_url+str_endpoint)
        else:
            return self.get(self.str_url+str_endpoint,str_filter)

    def gen_NETid(self,str_filter=None):
        dic_netdata   = {}
        str_endpoint = "/net"
        if str_filter == None:
            json_net = self.get(self.str_url+str_endpoint)
            for dic_tmp in json_net["data"]:
                dic_netdata.update({dic_tmp["id"]:dic_tmp["name"]})
            return dic_netdata
        else:
            json_net = self.get(self.str_url+str_endpoint,str_filter)
            for dic_tmp in json_net["data"]:
                if re.findall(str_filter,dic_tmp["name"]):
                    dic_netdata.update({dic_tmp["id"]:dic_tmp["name"]})
            return dic_netdata

    def get_NETIXLANinfo(self,str_filter=None):
        dic_data      = {"data":[]}
        str_endpoint  = "/netixlan"
        json_netixlan = self.get(self.str_url+str_endpoint)
        if str_filter == None:
            dic_ixid = self.gen_IXid()
            return json_netixlan
        else:
            dic_ixid = self.gen_IXid(str_filter)
            for dic_netixlan in json_netixlan["data"]:
                for int_target in dic_ixid.keys():
                    if int_target == dic_netixlan["ix_id"]:
                        dic_data["data"].append(dic_netixlan)
            return self.gen_db2json(dic_data)

################################################################################################

if __name__=='__main__':
    from   pprint   import *

    lst_ixtarget = ["JPIX", "BBIX", "JPNAP", "Equinix"]
    lst_ixport   = []

    o = PeeringDB()

    dic_ixid  = o.gen_IXid()
    dic_netid = o.gen_NETid()

    for str_ixtarget in lst_ixtarget:
        for dic_ixport in o.get_NETIXLANinfo(str_ixtarget)["data"]:
            lst_ixport.append([
                dic_ixid[dic_ixport["ix_id"]],
                dic_ixport["asn"],
                dic_ixport["net_id"],
                dic_netid[dic_ixport["net_id"]],
                dic_ixport["ipaddr4"],
                dic_ixport["ipaddr6"],
                dic_ixport["speed"],
            ])
    print lst_ixport

################################################################################################
