import sys
import re
import chardet

def zh_eng_2_zh(zh_eng_file,zh_file):
    "将中英字幕转换为中文字幕,去除英文部分(SRT)"

    encoding=''
    # detect file encoding
    with open(zh_eng_file, 'rb') as fd:
        raw = fd.read(1024) 
        encoding = chardet.detect(raw)['encoding']
    print('detect encoding:'+encoding)
    if encoding=='ascii':
        encoding='utf-8'

    with open(zh_eng_file,"r",encoding=encoding) as zh_eng:
        zh=open(zh_file,'w',encoding=encoding)
        for line in zh_eng.readlines():
            match=re.match("[a-zA-Z][a-zA-Z0-9\s.,]*",line)
            if not(match and match.start()==0 and match.end()==len(line)):
                zh.write(line)
        zh.close()

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("""argv example: xxx_zh_eng.srt xxx_zh.srt""")
        sys.exit(-1)
    zh_eng_2_zh(sys.argv[1],sys.argv[2])