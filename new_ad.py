# -*- coding: utf-8 -*

import time
import os
import requests
# from nose_htmloutput import HtmlOutput
# from apicommon.sendemail import SendMail
import subprocess
# from bs4 import BeautifulSoup

import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


APIFILE = './case/ads/'
# APIFILE = './test_headline_data.py'
def runnose(apifile):
    global filename_msg
    try:
        homedir = '/deploy/liuyabin/maimai_headline_atf/nose_tests_logs/'
        createtime = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
        filename = homedir + 'ads_result' + createtime + '.html'
        filename_msg = 'ads_result' + createtime + '.html'
        # result = os.popen("nosetests -v --with-html --html-file="+filename+" " + output).read()
        # cmd = "nosetests -v -a env=online --with-html --html-file=" + filename + " " + apifile
        cmd = "nosetests -v -a env=online " + apifile
        print('cmd', cmd)
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
        result = pipe.read()
        return createtime, filename, str(result), filename_msg
    except Exception as e:
        print(str(e))
        return False

def check_api_result(html_doc):

    if 'class="failed"' in html_doc:
        print('false')
        return False
    else:
        print('true')
        return True

def send(rnose):
    authors = ['hansijie']
    global content
    global subject
    global test_server
    test_server = 'http://kvm-test-nearline1:10010/'
    if rnose:
        attachcontent = rnose[1]
        content = '有上线操作！！，在' + rnose[0] + '进行了一次自动化测试,'
        subject = 'ads后端接口'
        run_result = False
        with open(attachcontent,'r') as f:
            attachfile = f.read()
            run_result = check_api_result(attachfile)
        # msg_list = test_server + report_file
        url = "https://open.feishu.cn/open-apis/bot/v2/hook/36bcba02-b56a-4d81-9e65-269b3f3afa52"
        content_md = "<font color=\"info\">ads</font>上线：构建"
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content_md,
                "mentioned_list": authors
            },
            "text": {
                # "content":   content + msg_list,
                "mentioned_list": authors
            }
        }
        if not run_result:
            subject = subject + '失败'
            content = content + '有失败的用例，请打开链接检查。'
            # data["text"]["content"] = content + msg_list
            data["markdown"]["content"] = content_md + "<font color=\"warning\">失败</font>。\n"
        else:
            subject = subject + '成功'
            content = content + '全部执行通过。'
            # data["text"]["content"] = content + msg_list
            data["markdown"]["content"] = content_md + "<font color=\"info\">成功</font>。\n"
            # data["markdown"]["content"] += "> 时间:<font color=\"comment\">%s</font>\n> [查看结果](%s) " %(rnose[0],
            # msg_list)
        requests.post(url, json=data, headers={"content-type": "application/json"})
    else:
        print('执行失败')


if __name__ == '__main__':
    rnose = runnose(APIFILE)
    print('rnose', rnose)
    # report_file = rnose[3]
    # send(rnose)

