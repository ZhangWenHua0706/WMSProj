import csv
import os

import pytest
from common.yaml_util import YamlUtil


class DataUtil:

    def csv_read(self, file_name):
        csv_list = []
        # 用例数据以字典的形式存入data_list
        data_list = []
        with open(os.getcwd() + '\\data\\' + file_name, mode='r', encoding='utf-8') as f:
            csv_line = csv.reader(f)
            for row in csv_line:
                csv_list.append(row)
            for i in range(1, len(csv_list)):
                case_dict = {}
                for j in range(0, len(csv_list[0])):
                    case_dict[csv_list[0][j]] = csv_list[i][j]
                data_list.append(case_dict)
        return data_list
