"""
约苗HPV 抢苗时间预览
目的：查看指定城市中哪些社区可预约，用做准备未来手动预约抢苗。


2019 7/18 最后修改
2020-04-22 00:36:49 测试可用
"""
import time
import hashlib
import requests
import pprint

_9PRICE = 8803
_4PRICE = 8802

class Yuemiao:
    def __init__(self, tk):
        self.tk = tk
        self.vaccineCode = _9PRICE
        # self.vaccineCode = 8803  # 疫苗代码 九阶HPV 8803
        # self.vaccineCode = 8802  # 疫苗代码 4阶HPV 8802
        pass


    def page_list(self,city_name='成都市'):
        '''医院社区列表'''
        uri = 'https://wx.healthych.com/base/department/pageList.do'
        params = {
            'cityName': city_name,
            'offset': 0,
            'limit': 300,  # 100
            'isOpen': 1,
            'longitude': '102.69378662109375',
            'latitude': '25.05844497680664',
            'vaccineCode': self.vaccineCode,
        }

        con = requests.get(uri, params=params, headers=self.headers())
        return con

    def headers(self):
        return {
            'st': self.build_st(),
            'tk': self.tk,
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.4(0x17000428) NetType/WIFI Language/zh_CN',
            'referer': 'https://wx.healthych.com/index.html'
        }

    def build_st(self):
        now_time = time.strftime('%Y%m%d%H%M')
        rel = now_time + 'jkzx705'
        m1 = hashlib.md5()
        m1.update(rel.encode("utf-8"))
        token = m1.hexdigest()
        return token

    def seckill_list(self,city_name='成都市'):
        '''可秒杀疫苗的医院列表'''
        rel = []

        list_hospital = m.page_list(city_name).json()
        # return  list_hospital
        assert list_hospital['ok'] and list_hospital['data']['rows'], ('列表数据错误：%s' % list_hospital['msg'])
        for item in list_hospital['data']['rows']:
            if item['isSeckill'] == 1:  # 秒杀图标
                rel.append((
                    item['code'],
                    item['name'],
                    self.vaccines_list(item['code'], self.vaccineCode)
                ))
        return rel

    def vaccines_list(self, depaCode, vaccineCode=''):
        '''
        获取医院的疫苗信息
        :param depaCode: 医院id
        :param vaccineCode: 疫苗id. 空字符串表示会获取所有疫苗列表
        :return:
        '''
        uri = 'https://wx.healthych.com/base/department/vaccines.do'
        params = {
            'depaCode': depaCode,
            'vaccineCode': vaccineCode,
        }
        content = requests.get(uri, headers=self.headers(), params=params).json()
        assert int(content['code']) == 0, '获取医院的疫苗信息错误'

        '''
        {"code":"0000","data":[{"code":"8803","name":"九价人乳头瘤病毒疫苗","intro":"人乳头瘤病毒（ HPV）高危亚型感染是宫颈癌的主要病因，99.8%的宫颈癌可检测出人类乳头瘤病毒DNA阳性。九价人乳头瘤病毒吸附疫苗，简称9价HPV疫苗。可预防16、18、31、33、45、52和58型引起的宫颈癌和其他癌前病变或不典型病变，以及预防6、11亚型引起的尖锐湿疣。","id":3702,"price":132800,"total":0,"isSeckill":1}],"ok":true}
        '''
        rel = []
        for item in content['data']:
            # item['id']#疫苗id
            info = self.__vaccine_info(item['id'])
            rel.append(info)
        return rel
    def __vaccine_info(self,id):
        '''
        获取疫苗信息
        :param id:疫苗id
        :return: dict{'time':'1970-01-01 00:00:00','desc':''}
        '''
        uri = 'https://wx.healthych.com/seckill/vaccine/detail.do'
        params = {
            'id':id
        }
        con = requests.get(uri,headers=self.headers(),params=params).json()
        '''
        {"code":"0000","data":{"id":3702,"name":"九价人乳头瘤病毒疫苗","total":0,"intro":"龙泉驿区第二批次九价人乳头瘤病毒的预约将于2019年4月26日14：00准时开放，敬请期待","describtion":"<p><img src=\"https://adultvacc-1253522668.file.myqcloud.com/thematic%20pic/%E4%B9%9D%E4%BB%B7_1533805007061.png\" alt=\"九价.png\"/></p>","startTime":"2019-04-26 14:00:00","startMilliscond":1556258400000,"now":1559129439884,"workTimeStart":"14：00","workTimeEnd":"16：00"},"ok":true}
        '''
        assert int(con['code']) == 0 and con['data'], ('疫苗信息获取失败:%s' % con['msg'])
        # if not (int(con['code']) == 0 and con['data']):#todo
        #     return {
        #         'time': '1970-01-01 00:00:00',
        #         'desc': con['msg'],
        #     }


        return {
            'time':con['data']['startTime'],#秒杀开始时间
            'desc':con['data']['intro'],#描述文本
        }

    def str2timestmap(self,str):
        time_tuple = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(time_tuple))
        return timestamp



if __name__ == '__main__':
    # m = Yuemiao('f7fe3c1798bfdc3b7809b97a42f37ba9_148c572780f03baa99faef0a7a05f2e3')
    m = Yuemiao('f7fe3c1798bfdc3b7809b97a42f37ba9_600655fa6b2ea4acd3ebd5236cb33264')
    citys = ['成都市','都江堰市','乐山市','峨眉山市','自贡市','雅安市','宜宾市','眉山市','绵阳市','重庆市','昆明市','荆门市']
    
    name_map = {
        _9PRICE:'九价HPV疫苗',
        _4PRICE:'四价HPV疫苗',
    }
    for vaccineCode in [_9PRICE,_4PRICE]:
        print(name_map[vaccineCode])
        ...

        for city in citys:
            try:
                m.vaccineCode = vaccineCode
                _list = m.seckill_list(city_name=city)
                now = int(time.time())

                rel = []#可预约列表
                for item in _list:
                    for info in item[2]:
                        t = m.str2timestmap(info['time'])
                        if t > now:#预约时间未到
                            rel.append((
                                info['time'],#预约时间
                                # info['desc'],#预约描述
                                item[1],#医院/社区名称
                            ))
                if rel:
                    pprint.pprint('---')
                    pprint.pprint('%s:'%city)#获取哪些可以预约的疫苗
                    pprint.pprint(rel)#获取哪些可以预约的疫苗
                else:
                    # pprint.pprint('...')
                    pass

            except AssertionError as e:
                raise e
            except KeyError as e:
                continue

