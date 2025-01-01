import re

# 规则文件路径
file_path = './rules.txt'

# 读取文件内容
with open(file_path, 'r', encoding='utf-8') as f:
    rules = [line.strip() for line in f if line.strip() and not line.startswith('!')]

# 检查规则是否为 AdGuard Home 支持的格式
def is_adguard_home_rule(rule):
    """检查规则是否为 AdGuard Home 支持的格式"""
    if rule.startswith('||'):
        return True
    if rule.startswith('|'):
        return True
    if rule.startswith('@@'):
        return True
    return False

# 过滤出仅 AdGuard Home 支持的规则
adguard_home_rules = [rule for rule in rules if is_adguard_home_rule(rule)]

# 用于存储最终规则的集合
blocked_rules = set()

# 仅存储屏蔽规则
for rule in adguard_home_rules:
    if not rule.startswith('@@'):  # 忽略允许规则
        blocked_rules.add(rule)

# 移除重复规则并按字母排序
final_rules = sorted(blocked_rules)

# 写回原文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(final_rules))
