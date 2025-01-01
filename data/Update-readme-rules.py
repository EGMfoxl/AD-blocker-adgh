import subprocess
from datetime import datetime
import pytz

# 获取当前北京时间
beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).isoformat(sep=' ', timespec='seconds')

file_path = "rules.txt"
# 读取文件内容并区分注释行和规则行
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()
comments = [line for line in lines if line.strip().startswith('!')]  # 注释行
filters = [line for line in lines if not line.strip().startswith('!')]  # 规则行
# 对规则行排序
filters.sort(key=lambda x: x.strip().lower())
# 合并注释和排序后的规则行
sorted_lines = comments + filters
# 写入排序后的内容
with open(file_path, "w", encoding="utf-8") as file:
    file.writelines(sorted_lines)
# 统计非注释行数
line_count = len(filters)

# 更新 README.md 中的规则计数和更新时间
subprocess.run(f"sed -i 's/^更新时间:.*/更新时间: {beijing_time} （北京时间） /g' README.md", shell=True)
subprocess.run(f"sed -i 's/^规则数量.*/规则数量: {line_count} /g' README.md", shell=True)

print("已更新README.md")
