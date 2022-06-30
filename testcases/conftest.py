import datetime
import json
import urllib

import pytest
from common.request_util import RequestUtil
from common.yaml_util import YamlUtil
from log.log_util import LogUtil


@pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
@pytest.fixture(scope="function")
def login(baseinfo):
    method = "post"
    post_type = "form"
    data = {
        "userName": baseinfo["base"]["userName"],
        "password": baseinfo["base"]["password"],
        "loginType": baseinfo["base"]["login_type"]
    }
    assert_str = baseinfo["base"]["assert_str"]
    rep = RequestUtil().send_request(method, baseinfo["base"]["login_url"], data, post_type)
    if str(assert_str) == str(json.loads(rep)["code"]):
        auth_header = baseinfo["base"]["pre_auth"] + " " + json.loads(rep)["data"]["authorization"]
        YamlUtil().write_extract_yaml("extract.yaml", auth_header)
        login_info = json.loads(rep)["data"]
        return login_info
    else:
        print("登录失败,请检查!")


@pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
@pytest.fixture(scope="function")
def getcustinfo(baseinfo,login):
    method = "get"
    data = None
    auth_header = YamlUtil().read_extract_yaml("extract.yaml")
    headers = {
        "authorization": auth_header}
    assert_str = baseinfo["base"]["assert_str"]
    log = LogUtil().log_free()
    rep = RequestUtil().send_request(method, baseinfo["base"]["getcust_url"], data,'',headers=headers)
    if str(assert_str) == str(json.loads(rep)["code"]):
        cust_info = json.loads(rep)["data"][0]
        log.info("获取客户列表成功")
        return cust_info
    else:
        log.info("获取客户列表失败,请检查!")


@pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
@pytest.fixture(scope="function")
def getgoodsinfo(baseinfo,getcustinfo):
    method = "get"
    data = {
        "type": 1,
        "page": 1,
        "limit": 20,
        "goodsEnable": 1,
        "goodsCustId": "",
        "goodsCustomerId": getcustinfo["custId"],
        "goodsCategoryId": "",
        "goodsName": "",
        "goodsExtendCode": "",
        "goodsCode": "",
        "goodsBarcode": ""
    }
    auth_header = YamlUtil().read_extract_yaml("extract.yaml")
    headers = {
        "authorization": auth_header }
    assert_str = baseinfo["base"]["assert_str"]
    log = LogUtil().log_free()
    rep = RequestUtil().send_request(method, baseinfo["base"]["getgood_url"], data,"", headers=headers)
    if str(assert_str) == str(json.loads(rep)["code"]):
        if len(json.loads(rep)["data"]["list"]) > 0:
            goods_info = json.loads(rep)["data"]["list"][0]
            log.info("获取商品列表成功")
            return goods_info
    else:
        log.info("获取商品列表失败,请检查!")


@pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
@pytest.fixture(scope="function")
def getinstorebilllist(baseinfo,login):
    method = "get"
    data = {
        "page": 1,
        "limit": 20,
        "isStuff": 0,
        "startTime": datetime.datetime.today().strftime('%Y-%m-%d')+" 00:00:00",
        "endTime": datetime.datetime.today().strftime('%Y-%m-%d')+" 23:59:59",
        "startTimeLocal": "",
        "endTimeLocal": "",
        "inbillOrgId": login["orgId"],
        "inbillCustName":"",
        "inbillStatus":"",
        "inbillType":"",
        "inbillNumber":"",
        "inbillCreateUserName":"",
        "goodsName":"",
        "inbillInfoBatchNumber":"",
        "inbillInfoOrderNo":"",
        "inbillRemark":"",
        "trayNumber":"",
        "inbillOrderNo":"",
        "inbillInfoReceiptUserName": ""
    }
    auth_header = YamlUtil().read_extract_yaml("extract.yaml")
    headers = {
        "authorization": auth_header }
    assert_str = baseinfo["base"]["assert_str"]
    log = LogUtil().log_free()
    rep = RequestUtil().send_request(method, baseinfo["base"]["getinstorebilllist_url"], data,"", headers=headers)
    if str(assert_str) == str(json.loads(rep)["code"]):
        if len(json.loads(rep)["data"]["list"]) > 0:
            instore_bill_list = json.loads(rep)["data"]["list"]
            log.info("获取入库单列表成功")
            return instore_bill_list
    else:
        log.info("获取入库单列表失败,请检查!")


@pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
@pytest.fixture(scope="function")
def getinstorebillinfo(baseinfo,getinstorebilllist):
    method = "get"
    data = None
    auth_header = YamlUtil().read_extract_yaml("extract.yaml")
    headers = {
        "authorization": auth_header }
    assert_str = baseinfo["base"]["assert_str"]
    log = LogUtil().log_free()
    url = baseinfo["base"]["getinstorebillinfo_url"]
    url = url + str(getinstorebilllist[0]["id"])
    rep = RequestUtil().send_request(method, url, data,"", headers=headers)
    if str(assert_str) == str(json.loads(rep)["code"]):
        if len(json.loads(rep)["data"]) > 0:
            instore_bill_info = json.loads(rep)["data"]
            log.info("获取入库单信息成功")
            return instore_bill_info
    else:
        log.info("获取入库单信息失败,请检查!")