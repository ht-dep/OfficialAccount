# coding: utf-8

import itchat
from itchat.content import *
import re
from settings import *
from OfficialAccount import OfficialAccount as OA


def handler(msg):
    print msg.Text
    # 找公众号
    if re.search(u'公众号', msg.Text):
        oa_name = msg.Text.strip().split(' ')[-1]

        # 找到
        if OA.search_oa(oa_name) and OA.get_max_page() != -1:
            print OA.max_page
            itchat.send(u'不吹不黑, {}页案底, 我都给您整好了, 页数小的是最近的, 想看哪页您就说'.format(OA.max_page), USERNAME)
            OA.get_page_urls()
            # print OA.page_urls[-1]
        # 没找到
        else:
            itchat.send(u'据小弟所知, 地球上没有这种生物', USERNAME)
    # 找页数
    else:
        try:
            page = re.match('\d+', msg.Text.strip())
            page_num = int(page.group())
            if page_num in range(1, OA.max_page+1):
                info = OA.get_article(OA.page_urls[page_num-1])
                reply_msg = ''
                for i in info:
                    print i[0], i[1]
                    reply_msg += i[0] + '\n' + i[1] + '\n'
                itchat.send(reply_msg.strip(), USERNAME)
            else:
                itchat.send(u'不是小弟才力不济, 他只有{}页案底啊'.format(OA.max_page), USERNAME)
        except:
            itchat.send(u'大哥, 你又欺负小弟了', USERNAME)


@itchat.msg_register(TEXT)
def reply(msg):
    if msg.ToUserName == USERNAME:
        handler(msg)


itchat.auto_login(True)
# 发送欢迎语
itchat.send(WELCOME, USERNAME)

itchat.run()


