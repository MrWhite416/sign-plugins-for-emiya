# 开发时间：2023/10/23  15:05
# The road is nothing，the end is all    --Demon
import random
import base64

import time

from jinja2 import Environment, FileSystemLoader
from html2image import Html2Image
from libs.event.qqevent import onkeyword


# 加载html
def generate_html(res):
    env = Environment(loader=FileSystemLoader('./'))  # './'表示从上一级目录加载模版
    template = env.get_template('plugins/SignIn/signin.html')  # 加载名为'signin.html'的模板。

    with open("plugins/SignIn/result.html", 'w+', encoding='utf8') as f:
        html_content = template.render(dic=res)  # 将参数res传递给模板进行渲染
        f.write(html_content)  # 渲染后的HTML内容写入到"result.html"文件中
    # print(type(html_content))

# html转图片
def convert():
    hti = Html2Image(size=(400, 600))
    hti.output_path = 'plugins/SignIn/'  # 设置输出路径
    hti.screenshot(other_file='plugins/SignIn/result.html', save_as='signin.jpg')  # 图片已被保存在目录

def parameter():
    # 获取模版中需要的参数
    now_time = time.time()
    n_time = time.localtime(now_time)
    t = time.strftime("%m/%d %H:%M:%S", n_time)  # 获取当前日期
    t1,t2 = t.split(' ')
    x = random.randint(0,9)
    y = random.randint(0,9)
    gd = '您好'
    if int(t[-8:-6])<9:  # 时间早于九点则是早上好
        gd = '早上好'
    elif int(t[-8:-6])<11:  # 上午好
        gd = '上午好'
    elif int(t[-8:-6])<13:  # 中午好
        gd = '中午好'
    elif int(t[-8:-6])<17:  # 下午好
        gd = '下午好'
    elif int(t[-8:-6])<19:  # 傍晚好
        gd = '傍晚好'
    elif int(t[-8:-6])<24:  # 晚上好
        gd = '晚上好'

    with open('plugins/SignIn/entry.josn', 'r',encoding='utf8') as f:
        da = eval(f.read())
        lst = random.sample(da,4)
        del lst[0]['bad']  # 删除字典的忌
        del lst[1]['good'] # 删除字典的宜
        del lst[2]['bad']  # 删除字典的忌
        del lst[3]['good']  # 删除字典的宜
        good1 = lst[0]['name']+' -- '+lst[0]['good']
        good2 = lst[2]['name']+' -- '+lst[2]['good']
        bad1 = lst[1]['name']+' -- '+lst[1]['bad']
        bad2 = lst[3]['name']+' -- '+lst[3]['bad']


        print(good1)

    return good1,good2,bad1,bad2,gd,t1,t2,x,y

# 图片转为base64码的函数，需要将传入一个图片路径
def encode_images_to_base64():
    base64_images = []  # 存储处理后的 Base64 字符串

    with open('plugins/SignIn/signin.jpg', 'rb') as file:  # 以二进制读取模式（'rb'）打开当前图片文件。
        encoded_string = base64.b64encode(file.read()).decode('utf-8')  # 读取打开的文件内容，并使用 base64.b64encode 将其编码为 Base64 格式的字符串。
        # 然后使用 decode('utf-8') 将二进制格式的 Base64 字符串转换为人类可读的字符串
        base64_images.append(encoded_string)  # 将编码后的 Base64 字符串添加到 base64_images 列表中。

    return base64_images  # 函数返回包含所有 Base64 字符串的列表


@onkeyword(keywordList=["@签到"])
async def handle(n):
    good1,good2,bad1,bad2,gd,t1,t2,x,y = parameter()  # 问候，时间，钱，好感

    res = {'good': gd, 'time_M': t1, 'time_S': t2, 'name': n.netpackage.getSender().nickname, 'addCoin': x, 'signDay': 100, 'favorability': y
            ,'coin': 10, 'yes': [good1, good2], 'no': [bad1, bad2]
              }

    generate_html(res)
    convert()
    pic_base64 = encode_images_to_base64()[0]

    CQ_code = f'[CQ:image,file=base64://{pic_base64}]'
    rp = await n.callAPI(url="send_group_msg", group_id=n.netpackage.getID(), message=CQ_code)

if __name__ == '__main__':
    parameter()



