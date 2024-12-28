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
allowed_rules = set()
blocked_rules = set()

# 分别存储允许规则和屏蔽规则
for rule in adguard_home_rules:
    if rule.startswith('@@'):
        allowed_rules.add(rule)
    else:
        blocked_rules.add(rule)

# 去除冲突规则：如果允许规则存在，则删除相应的屏蔽规则
final_rules = set()

for blocked_rule in blocked_rules:
    # 查找屏蔽规则对应的允许规则
    if blocked_rule.startswith('||'):
        exception_rule = '@@' + blocked_rule
    elif blocked_rule.startswith('|'):
        exception_rule = '@@' + blocked_rule
    else:
        exception_rule = None
    
    # 如果对应的允许规则存在，忽略该屏蔽规则
    if exception_rule not in allowed_rules:
        final_rules.add(blocked_rule)

# 添加所有的允许规则
final_rules.update(allowed_rules)

# 移除重复规则并按字母排序
final_rules = sorted(final_rules)

# 写回原文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(final_rules))
