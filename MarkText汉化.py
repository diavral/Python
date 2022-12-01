#!coding:utf-8
# filename:  MarkText汉化
# author:    1
# created:   2022/12/1の15:22
# project:   Python3.8
# idea:      PyCharm
# finished:  2022/12/1 23:52 汉化失败，resources/app.asar 文件的信息被硬编码了，只能等长的翻译(更换大小写这种等长操作不报错)
# 标准库
import os
# 第三方库

# 模块
import re

mark_text_app_asar_dir = r'E:\marktext0151\Mark Text\resources'   #  版本:0.15.1.1354
# file_row_file = os.path.join(os.path.abspath(os.path.curdir), "a.pak")  # 输入源
file_row_file = os.path.join(os.path.abspath(mark_text_app_asar_dir), "app-待翻译副本.asar")  # 输入源

file_to_translate = "0a-temp-translate.txt"  # 用于翻译的中间文件
file_to_translate_separator = '---translated---'.encode()
file_to_translate_placeholder = '䶮'.encode()
local_words_left = '['.encode()  # associate with regex,maybe need to modify label_content_regex
local_words_right = ']'.encode()

outdir =mark_text_app_asar_dir+os.path.sep+"app.asar"  # 输出文件



def temp_read_file():
    with open(file_row_file, 'rb') as f:
        content = f.read()

        # label_regex = re.compile(rb'label:"[^"]+?"[,}]{1,2}')
        label_regex = re.compile(rb'label:"[^"]+?"')
        label_content_regex = re.compile(rb'"[^"]+?"')
        labels = label_regex.findall(content)

        # for label in labels:
        #     print(label,label.decode())
        with open(file_to_translate, 'wb') as f2:
            for label in labels:
                # label_content=label_content_regex.findall(label)[0].replace(b'"',b'')
                label_content = label_content_regex.findall(label)[0].replace(b'"', b'')+file_to_translate_separator+local_words_left+file_to_translate_placeholder+local_words_right
                f2.write(label_content+b'\n')

def temp_write_bug():
    file_pointer = 0
    write_pointer = 0
    write_pointer_before = 0

    with open(file_to_translate,'rb')  as f ,open(outdir,"wb") as output_file,open(file_row_file,"rb") as input_file:
        labels = f.readlines()
        read_content =input_file.read()
        write_content = b''
        for label in labels:
            # label_content_regex = re.compile(rb'\[[^'+local_words_right+rb']+?\]')
            label_content_regex = re.compile(b'\\'+local_words_left+rb'[^'+local_words_right+rb']+?'+b'\\'+local_words_right)
            label_content = label_content_regex.findall(label)[0].replace(local_words_left,b'').replace(local_words_right,b'')

            # label_content_regex_default = re.compile(rb'\[[^\]]+?\]')
            # label_content_default = label_content_regex_default.findall(label)[0].replace(local_words_left,b'').replace(local_words_right,b'')
            # print(label_content_default ==label_content,label_content,label_content_default)

            label_content_key=label[:label.find(file_to_translate_separator+local_words_left)]
            keyword = b'label:"'
            file_pointer = read_content.find(keyword,file_pointer)+len(keyword)
            search_result = read_content[file_pointer:read_content.find(b'"',file_pointer)]
            # print(search_result==label_content_key,search_result ,'<->', label_content_key)
            # read_content[file_pointer:read_content.find(b'"', file_pointer)] =label_content
            # read_content[file_pointer:read_content.find(b'"', file_pointer)]
            write_pointer=file_pointer  # 包括keyword
            # write_content+=(read_content[write_pointer_before:write_pointer]+label_content_key.decode().upper().encode())


            if len(label_content)==len(label_content_key):
                # print(len(label_content)==len(label_content_key),label_content,label_content_key)
                write_content += (read_content[write_pointer_before:write_pointer] + label_content)
                write_pointer_before = file_pointer + len(search_result)

            else:
                print("翻译后文本编码长度和源文本不等长，无法更换")
                print(f'[{label_content.decode()}]译长：{len(label_content)}' ,f'[{label_content_key}]源长：{ len(label_content_key)}',f'编码：[{ label_content}]', sep="\t\t")
                write_content += (read_content[write_pointer_before:write_pointer] + label_content_key)
                write_pointer_before = file_pointer + len(search_result)

            # file_pointer = write_content.index(keyword, file_pointer) + len(keyword)
        write_content += read_content[write_pointer_before:]

        output_file.write(write_content)

temp_read_file()
temp_write_bug()



