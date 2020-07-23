from googletrans import Translator
import chardet
import re
import sys

def en_2_zh_eng(en_file,zh_en_file):
    "将英文字幕转换为中英字幕,翻译英文部分(SRT)"
    encoding=''
    
    # detect file encoding
    with open(en_file, 'rb') as file:
        raw = file.read(128) 
        encoding = chardet.detect(raw)['encoding']
    print('detect encoding:'+encoding)
    
    translator=Translator(service_urls=['translate.google.cn']) 

    if encoding=='ascii':
        encoding='utf8'
    en_fd=open(en_file,'r',encoding=encoding)
    lines=en_fd.readlines()
    en_fd.close()
    zh_en_fd=open(zh_en_file,'w',encoding=encoding)

    flag = False
    en_str=''
    index=1

    total_lines=str(len(lines))
    for line in lines:
        print(str(index)+'/'+total_lines)
        index+=1
        match=re.match("[a-zA-Z][a-zA-Z0-9\s.,]*",line)
        if not(match and match.start()==0 and match.end()==len(line)):
            if flag:
                flag=False
                print(en_str)
                zh_en_fd.write(translator.translate(en_str,dest='zh-CN').text+'\n')
                zh_en_fd.write(en_str)
                zh_en_fd.write(line)
            else:
                zh_en_fd.write(line)
        else:
            if flag:
                if len(en_str)>0 and en_str[-1]=='\n':
                    en_str=en_str[0:-1]+' '
                en_str=en_str+line
            else:
                flag=True
                en_str=line

    if flag:
        zh_en_fd.write(translator.translate(en_str,dest='zh-CN').text)
        zh_en_fd.write(en_str)
        zh_en_fd.write(line)

    zh_en_fd.close()    


if __name__=='__main__':
    if len(sys.argv)!=3:
        print("""argv example: xxx_eng.srt xxx_zh.srt""")
        sys.exit(-1)
    en_2_zh_eng(sys.argv[1],sys.argv[2])
    
