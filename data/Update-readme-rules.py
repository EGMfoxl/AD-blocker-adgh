import subprocess
import datetime
import pytz

# 获取当前时间并转换为北京时间
time = datetime.datetime.now(pytz.timezone('UTC'))
beijing_time = time.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

# 指定 rules.txt 文件路径
file_path = 'rules.txt'

# 打开文件并读取内容
with open(file_path, 'r') as file:
    content = file.read()

# 计算文件的行数
line_count = content.count('\n') + 1

# 在文件顶部插入内容
new_content = f"[Adblock Plus 2.0]\n" \
              f"! Title: MYSEIF\n" \
              f"! Homepage: https://github.com/EGMfoxl/AD-blocker-adgh\n" \
              f"! Expires: 12 Hours\n" \
              f"! Version: {beijing_time}（北京时间）\n" \
              f"! Description: 适用于AdGuard的去广告规则，合并优质上游规则并去重整理排列\n" \
              f"! Total count: {line_count}\n" \
              f"{content}"

# 将更新后的内容写入文件
with open(file_path, 'w') as file:
    file.write(new_content)

# 更新 README.md 中的规则计数和更新时间
subprocess.run(f"sed -i 's/^更新时间:.*/更新时间: {beijing_time} （北京时间） /g' README.md", shell=True)
subprocess.run(f"sed -i 's/^规则数量.*/规则数量: {line_count} /g' README.md", shell=True)

print("已成功更新 rules.txt 和 README.md 中的内容")
