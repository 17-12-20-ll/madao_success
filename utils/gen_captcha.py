import io
import random
import string

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ---------------------获取图形验证码----------------------

# 设置验证码的位数
number = 4
# 生成验证码图片的高度和宽度，可以依据实际情况选择
size = (70, 28)
# 背景颜色，默认为白色
bgcolor = (255, 255, 255)
# 字体颜色，默认为蓝色
fontcolor = (204, 70, 126)
# 干扰线颜色。默认为红色
linecolor = (255, 0, 0)
# 是否要加入干扰线
draw_line = False
# 加入干扰线条数的上下限
line_number = (1, 3)


# 获取随机字串作为验证码
def gen_text():
    source = list(string.ascii_letters + string.digits)
    # number是生成验证码的位数
    return ''.join(random.sample(source, number))


# 用来绘制干扰线
def gene_line(draw, width, height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill=linecolor)


# 获取图片验证码
def get_captcha():
    # 生成字符串，得到随机数字与字母组合
    text = gen_text()
    width, height = size  # 宽和高
    # 创建图片
    image = Image.new('RGBA', (width, height), bgcolor)
    # 验证码的字体和字体大小
    # 当前模块启动：path = ../static/fonts/ALKATIP_Elipbe_Tom.ttf，服务器启动使用根路径
    font = ImageFont.truetype('static/fonts/ALKATIP_Elipbe_Tom.ttf', size=25)
    # 创建画笔
    draw = ImageDraw.Draw(image)
    font_width, font_height = font.getsize(text)
    # 讲字符串写到图片上
    draw.text(
        ((width - font_width) / number,
         (height - font_height) / number),
        text, font=font, fill=fontcolor)  # 填充字符串
    
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    
    # 绘制干扰线段
    if draw_line:
        for _ in line_number:
            gene_line(draw, width, height)
    # image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  # 创建扭曲
    # 滤镜，边界加强
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # 释放画笔
    del draw
    # 将图片保存然后返回给用户
    # 直接内存文件操作，将图片数据返回，不用担心验证码图片过多
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    image.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return {'img': buf.getvalue(), 'text': text}


if __name__ == '__main__':
    print(get_captcha())
