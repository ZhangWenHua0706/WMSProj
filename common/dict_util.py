

class DictUtil:
    def dict_handle_noindex(self, dic1, dic2):
        for i in dic1.keys():
            if isinstance(dic1[i], list):
                for j in dic1[i]:
                    if isinstance(j, dict):
                        j = self.dict_handle_noindex(j, dic2)
                    else:
                        continue
            elif isinstance(dic1[i], dict):
                dic1[i] = self.dict_handle_noindex(dic1[i], dic2)
            elif i == "id":
                dic1[i] = ""
                continue
            else:
                for data_key in dic2.keys():
                    if i == data_key:
                        if dic2[data_key] == "null":
                            dic1[i] = ""
                        else:
                            dic1[i] = dic2[data_key]
                        break
                    else:
                        continue
        return dic1

    def dict_handle_index(self, dic1, dic2, index_num=0):
        for i in dic1.keys():
            if isinstance(dic1[i], list):
                if dic1[i]:
                    for j in dic1[i]:
                        index_num = dic1[i].index(j)
                        if isinstance(j, dict):
                                j = self.dict_handle_index(j, dic2,index_num)
                        else:
                            continue
                else:
                    continue
            elif isinstance(dic1[i], dict):
                dic1[i] = self.dict_handle_index(dic1[i], dic2,index_num)
            else:
                for data_key in dic2.keys():
                    if index_num > 0:
                        if str(i)+str(index_num) == data_key:
                            if dic2[data_key] == "null" and str(dic1[i]).startswith("$csv"):
                                dic1[i] = ""
                            elif dic2[data_key] == "null" and not str(dic1[i]).startswith("$csv"):
                                continue
                            else:
                                dic1[i] = dic2[data_key]
                            break
                        else:
                            continue
                    else:
                        if i == data_key:
                            if dic2[data_key] == "null":
                                dic1[i] = ""
                            else:
                                dic1[i] = dic2[data_key]
                            break
                        else:
                            continue
        return dic1

    def dict_handle_index1(self, dic1, dic2, index_num=0,index_num1=0):
        for i in dic1.keys():
            if isinstance(dic1[i], list):
                for j in dic1[i]:
                    index_num = dic1[i].index(j)
                    if isinstance(j, dict):
                            j = self.dict_handle_index1(j, dic2,index_num,index_num1)
                    else:
                        continue
            elif isinstance(dic1[i], dict):
                dic1[i] = self.dict_handle_index1(dic1[i], dic2,index_num,index_num1)
            elif i == "id":
                dic1[i] = ""
                continue
            else:
                for data_key in dic2.keys():
                    if isinstance(dic2[data_key], list):
                        for k in dic2[data_key]:
                            index_num1 = dic2[data_key].index(k)
                            if isinstance(k,dict):
                                dic1 = self.dict_handle_index1(dic1, k, index_num, index_num1)
                            else:
                                continue
                    elif isinstance(dic2[data_key], dict):
                        dic1 = self.dict_handle_index1(dic1, dic2[data_key], index_num, index_num1)
                    else:
                        if index_num > 0:
                            if str(i)+str(index_num) == data_key:
                                if dic2[data_key] == "null":
                                    dic1[i] = ""
                                else:
                                    dic1[i] = dic2[data_key]
                                break
                            else:
                                continue
                        else:
                            if i == data_key:
                                if dic2[data_key] == "null":
                                    dic1[i] = ""
                                else:
                                    dic1[i] = dic2[data_key]
                                break
                            else:
                                continue
        return dic1

    def dict_copy(self, dic1, dic2):
        for i in dic1.keys():
            if isinstance(dic1[i], list):
                if dic1[i]:
                    for j in dic1[i]:
                        index_num = dic1[i].index(j)
                        if isinstance(j, dict):
                                j = self.dict_copy(dic1[i][index_num], dic2[i][index_num] )
                        else:
                            continue
                else:
                    continue
            elif isinstance(dic1[i], dict):
                dic1[i] = self.dict_copy(dic1[i], dic2[i])
            else:
                for data_key in dic2.keys():
                    if i == data_key:
                        dic1[i] = dic2[data_key]
                        break
                    else:
                        continue
        return dic1

    def search_key(self, dic1, dic2):
        for data_key in dic2.keys():
            for i in dic1.keys():
                if i == data_key:
                    dic1[i] = dic2[data_key]
                    return dic1[i]


