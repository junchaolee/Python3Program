# coding:utf-8
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

'''
PDF转Word功能所需要的依赖包如下
PDFParser（文档分析器）
PDFDocument（文档对象）
PDFResourceManager（资源管理器）
PDFPageInterpreter（解释器）
PDFPageAggregator（聚合器）
LAParams（参数分析器）
整体思路：构造文档对象，解析文档对象，提取所需要内容
'''


def parse():
    # rb以二进制读模式打开本地PDF文件
    fp = open('test.pdf', 'rb')

    # 创建pdf文档分析器
    parser = PDFParser(fp)
    # 创建pdf文档对象
    doc = PDFDocument()

    # 连接分析器与文档对象
    parser.set_document(doc)
    doc.set_parser(parser)

    # 提供初始化密码，没有就创建一个空的字符串
    # doc.initialize("ipythonlianxi")
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDF资源管理器 来管理共享资源
        resource = PDFResourceManager()
        # 创建一个PDF参数分析器
        laparams = LAParams()
        # 创建聚合器，用于读取文档对象
        device = PDFPageAggregator(resource, laparams=laparams)
        # 创建解释器，对文档编码，解释成python能识别的格式
        interpreter = PDFPageInterpreter(resource, device)
        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages()获取page列表
        for page in doc.get_pages():
            # 利用解释器的process_page()方法解析读取单独页数
            interpreter.process_page(page)
            # 使用聚合器get_result()方法获取内容
            layout = device.get_result()
            # 这里的layout是一个LTpage对象，里面存放着整个page解析出的各种对象
            for out in layout:
                # 判断是否含有get_text()方法，获取我们想要的文字
                # if hasattr(out,"get_text"):
                #     print (out.get_text())
                #     with open('text.txt','a') as f:
                #         f.write(out.get_text()+'\n')
                if (isinstance(out, LTTextBoxHorizontal)):
                    with open('test.txt', 'a') as f:
                        results = out.get_text()
                        print(results)
                        f.write(results + '\n')


if __name__ == '__main__':
    parse()
