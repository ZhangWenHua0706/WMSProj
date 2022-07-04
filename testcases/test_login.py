import json
import re
import pytest
import requests
import allure
from common.data_util import DataUtil
from common.dict_util import DictUtil
from common.request_util import RequestUtil
from common.yaml_util import YamlUtil
from log.log_util import LogUtil


class TestLogin:
    session = requests.session()

    @allure.feature('访问首页')
    @pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
    def test_access(self, baseinfo):
        url = baseinfo['base']['index_url']
        data = ""
        rep = RequestUtil().send_request("get", url, data, None)
        pattern = r"<h1 id=\"title\">(.*)</h1>"
        log = LogUtil().log_info('访问首页')
        log.info('访问首页')
        log.info("预期测试结果返回:科驿智慧仓储管理平台")
        log.info("实际测试结果返回:" + str(re.search(pattern,rep).group(1)))
        assert '科驿智慧仓储管理平台' in rep

    @allure.feature('登录测试')
    @pytest.mark.parametrize('caseinfo', YamlUtil().read_test_yamlfile('test_login.yaml'))
    @pytest.mark.parametrize('baseinfo', YamlUtil().read_yamlfile('config.yaml'))
    @pytest.mark.parametrize('datainfo', DataUtil().csv_read('test_login.csv'))
    def test_login(self, baseinfo, caseinfo, datainfo):
        method = caseinfo["requests"]["method"]
        post_type = "form"
        last_url = baseinfo["base"]["base_url"] + caseinfo["requests"]["url"]
        data = caseinfo["requests"]["data"]
        data = DictUtil().dict_handle_index(data, datainfo)
        assert_str = DictUtil().search_key(caseinfo["validate"], datainfo)
        rep = RequestUtil().send_request(method, last_url, data, post_type)
        log = LogUtil().log_info(datainfo["name"])
        log.info(datainfo["story"])
        log.info("预期测试结果返回:"+datainfo["assert_str"])
        log.info("实际测试结果返回:"+str(json.loads(rep)["code"]))
        allure.dynamic.story(datainfo["story"])
        pytest.assume(assert_str in rep)
        if baseinfo["base"]["assert_str"] == str(json.loads(rep)["code"]):
            auth_header = baseinfo["base"]["pre_auth"] + " " + json.loads(rep)["data"]["authorization"]
            YamlUtil().write_extract_yaml("extract.yaml", auth_header)
        else:
            pass






