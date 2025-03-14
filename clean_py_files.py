import os
import re
import codecs

def clean_file(file_path):
    # 尝试不同的编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']
    content = None
    
    for encoding in encodings:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        raise Exception(f"无法使用任何已知编码读取文件")
    
    # 移除编码声明和shebang
    content = re.sub(r'^#!.*\n', '', content)
    content = re.sub(r'^#.*coding[:=].*\n', '', content)
    content = re.sub(r'^#.*-\*-.*-\*-.*\n', '', content)
    
    # 使用检测到的编码写回文件
    with codecs.open(file_path, 'w', encoding=encoding) as f:
        f.write(content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                try:
                    clean_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

if __name__ == '__main__':
    process_directory('.') 