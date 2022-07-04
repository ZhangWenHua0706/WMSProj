import json
import os

import pytest
import requests
import allure
import datetime
from common.data_util import DataUtil
from common.dict_util import DictUtil
from common.request_util import RequestUtil
from common.yaml_util import YamlUtil
from log.log_util import LogUtil


class TestOrderManage:
    session = requests.session()

    @allure.feature('创建入库单测试')
    @pytest.mark.parametrize('caseinfo', YamlUtil().read_test_yamlfile('test_instore_bill_add.yaml'))
    @pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
    @pytest.mark.parametrize('datainfo', DataUtil().csv_read('test_instore_bill_add.csv'))
    def test_instore_bill_add(self, baseinfo, caseinfo, datainfo,login,getcustinfo,getgoodsinfo):
        # 新建入库单
        method = caseinfo["requests"]["method"]
        post_type = "json"
        # 获取请求url
        last_url = baseinfo["base"]["base_url"] + caseinfo["requests"]["url"]
        # 初始化日志对象
        log = LogUtil().log_info(datainfo["name"])
        # 获取yaml文件里的入库单结构
        bill_info = caseinfo["requests"]["data"]
        # 将csv文件的测试数据赋值到入库单的对应字段
        if datainfo:
            bill_info = DictUtil().dict_handle_index(bill_info, datainfo)
        else:
            log.info("获取csv用例数据失败")
            return
        # 将登录用户信息赋值到入库单的对应字段
        if login:
            bill_info["inbillOrgId"] = login["orgId"]
            bill_info["inbillCreateUserName"] = login["username"]
            bill_info["inbillCreateUserId"] = login["id"]
        else:
            log.info("登录信息异常")
            return
        # 将客户信息赋值到入库单的对应字段
        if getcustinfo:
            bill_info = DictUtil().dict_handle_index(bill_info, getcustinfo)
            bill_info["inbillCustomerId"] = getcustinfo["custId"]
            bill_info["inbillCustId"] = getcustinfo["id"]
            bill_info["inbillCustName"] = getcustinfo["custName"]
            bill_info["goodsCustomerId"] = getcustinfo["custId"]
        else:
            log.info("获取客户信息失败")
            return
        # 将商品信息赋值到入库单的对应字段
        if getgoodsinfo:
            bill_info = DictUtil().dict_handle_noindex(bill_info, getgoodsinfo)
            bill_info["infos"][0]["inbillInfoReceiptUserId"] = login["id"]
            bill_info["infos"][0]["inbillInfoReceiptUserName"] = login["username"]
            bill_info["infos"][0]["inbillInfoGoodsId"] = getgoodsinfo["goodsId"]
            bill_info["infos"][1]["inbillInfoReceiptUserId"] = login["id"]
            bill_info["infos"][1]["inbillInfoReceiptUserName"] = login["username"]
            bill_info["infos"][1]["inbillInfoGoodsId"] = getgoodsinfo["goodsId"]
        else:
            log.info("获取商品列表失败")
            return
        # 赋值制单时间
        if bill_info["inbillCreateTime"]:
            pass
        else:
            bill_info["inbillCreateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 赋值入库时间
        if bill_info["inbillTime"]:
            pass
        else:
            bill_info["inbillTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取csv文件中预期结果数据
        assert_str = DictUtil().search_key(caseinfo["validate"], datainfo)
        auth_header = YamlUtil().read_extract_yaml("extract.yaml")
        headers = {
            "authorization":auth_header}
        # 发送创建入库单请求
        rep = RequestUtil().send_request(method, last_url, bill_info, post_type, headers=headers)
        log.info(datainfo["story"])
        log.info("预期测试结果返回:"+datainfo["assert_str"])
        log.info("实际测试结果返回:"+str(json.loads(rep)["code"]))
        allure.dynamic.story(datainfo["story"])
        pytest.assume(assert_str in rep)

    @allure.feature('修改入库单测试')
    @pytest.mark.parametrize('caseinfo', YamlUtil().read_test_yamlfile('test_instore_bill_update.yaml'))
    @pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
    @pytest.mark.parametrize('datainfo', DataUtil().csv_read('test_instore_bill_update.csv'))
    def test_instore_bill_update(self, baseinfo, caseinfo, datainfo, login, getinstorebillinfo):
        #修改入库单
        method = caseinfo["requests"]["method"]
        post_type = "json"
        # 获取请求url
        last_url = baseinfo["base"]["base_url"] + caseinfo["requests"]["url"]
        log = LogUtil().log_info(datainfo["name"])
        # 获取yaml文件里的入库单对象
        bill_info = caseinfo["requests"]["data"]
        # 将csv文件的测试数据赋值到入库单的对应字段
        if getinstorebillinfo:
            bill_info = DictUtil().dict_copy(bill_info,getinstorebillinfo)
        else:
            log.info("获取入库单信息失败")
        # 将csv文件的测试数据赋值到入库单的对应字段
        if datainfo:
            bill_info = DictUtil().dict_handle_index(bill_info, datainfo)
        else:
            log.info("获取csv用例数据失败")
            return
        # 将登录用户信息赋值到入库单的对应字段
        if login:
            bill_info["inbillOrgId"] = login["orgId"]
            bill_info["inbillCreateUserName"] = login["username"]
            bill_info["inbillCreateUserId"] = login["id"]
        else:
            log.info("登录信息异常")
            return
        # 赋值制单时间
        if bill_info["inbillCreateTime"]:
            pass
        else:
            bill_info["inbillCreateTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 赋值入库时间
        if bill_info["inbillTime"]:
            pass
        else:
            bill_info["inbillTime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 获取csv文件的预期结果
        assert_str = DictUtil().search_key(caseinfo["validate"], datainfo)
        auth_header = YamlUtil().read_extract_yaml("extract.yaml")
        headers = {
            "authorization": auth_header}
        # 发送请求
        rep = RequestUtil().send_request(method, last_url, bill_info, post_type, headers=headers)
        log.info(datainfo["story"])
        log.info("预期测试结果返回:" + datainfo["assert_str"])
        log.info("实际测试结果返回:" + str(json.loads(rep)["code"]))
        allure.dynamic.story(datainfo["story"])
        pytest.assume(assert_str in rep)


    @allure.feature('入库单导入测试')
    @pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
    def atest_instore_bill_import(self, login, baseinfo):
        # 导入入库单
        method = "post"
        post_type = "file"
        last_url = baseinfo["base"]["import_insotre_bill_url"]
        log = LogUtil().log_info("入库单导入")
        # 初始化导入文件
        files = {'excelFile': (baseinfo["base"]["import_insotre_bill_file"], open(os.getcwd() + '\\data\\' + baseinfo["base"]["import_insotre_bill_file"], 'rb'))}
        # 获取配置文件的预期结果
        assert_str = baseinfo["base"]["assert_str"]
        auth_header = YamlUtil().read_extract_yaml("extract.yaml")
        headers = {
            "authorization":auth_header}
        rep = RequestUtil().send_request(method, last_url, files, post_type,headers=headers)
        log.info("入库单导入")
        log.info("预期测试结果返回:"+str(assert_str))
        log.info("实际测试结果返回:"+str(json.loads(rep)["code"]))
        allure.dynamic.story("入库单导入")
        pytest.assume(str(assert_str) in rep)




