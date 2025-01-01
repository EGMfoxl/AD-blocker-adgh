# 文件路径
file_path = './rules.txt'

# 读取、过滤、写回文件
with open(file_path, 'r', encoding='utf-8') as f:
    rules = [line.strip() for line in f if line.strip() and not line.startswith('@@') and not line.startswith('!')]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(sorted(rules)))
