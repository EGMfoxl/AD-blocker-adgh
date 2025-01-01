import subprocess
from datetime import datetime
import pytz

# 获取当前北京时间
beijing_time = datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

# 指定 rules.txt 文件路径
file_path = 'rules.txt'

# 计算文件的行数
with open(file_path, 'r') as file:
    line_count = sum(1 for _ in file)

# 更新 README.md 中的规则计数和更新时间
subprocess.run(f"sed -i 's/^更新时间:.*/更新时间: {beijing_time} （北京时间） /g' README.md", shell=True)
subprocess.run(f"sed -i 's/^规则数量.*/规则数量: {line_count} /g' README.md", shell=True)

print("已成功更新 rules.txt 和 README.md 中的内容")
