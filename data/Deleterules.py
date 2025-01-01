# 规则文件路径
file_path = './rules.txt'

# 读取并处理规则文件
with open(file_path, 'r', encoding='utf-8') as f:
    rules = {line.strip() for line in f if line.strip() and not line.startswith(('!', '@@'))}

# 排序规则并写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(sorted(rules)))
