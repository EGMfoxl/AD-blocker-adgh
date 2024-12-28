import re
from collections import defaultdict


def parse_rule(rule):
    """解析规则，返回规则类型和主体"""
    if rule.startswith('||'):
        return 'domain', rule[2:]  # 域名规则
    elif rule.startswith('|'):
        return 'exact', rule[1:]  # 精确匹配
    elif rule.startswith('#@#'):
        return 'exception_css', rule[3:]  # CSS 例外规则
    elif rule.startswith('##'):
        return 'css', rule[2:]  # CSS 阻止规则
    elif rule.startswith('@@'):
        return 'exception', rule[2:]  # 例外规则
    else:
        return 'generic', rule  # 通用规则


def group_rules(rules):
    """按规则类型分组"""
    grouped = defaultdict(list)
    for rule in rules:
        rule_type, body = parse_rule(rule)
        grouped[rule_type].append((rule, body))
    return grouped


def remove_exact_duplicates(rules):
    """移除完全重复的规则"""
    return list(set(rules))


def remove_subsumed_domain_rules(domain_rules):
    """移除被包含的域名规则"""
    # 使用前缀树处理包含关系
    trie = {}
    for rule, domain in domain_rules:
        node = trie
        for part in domain.split('.'):
            if part not in node:
                node[part] = {}
            node = node[part]
        node['__end__'] = rule

    # 从前缀树提取最小规则集
    def extract_rules(node):
        if '__end__' in node:
            return [node['__end__']]
        rules = []
        for key, child in node.items():
            if key != '__end__':
                rules.extend(extract_rules(child))
        return rules

    return extract_rules(trie)


def remove_redundant_css_rules(css_rules):
    """移除冗余 CSS 规则"""
    cleaned = set(css_rules)
    for rule, selector in css_rules:
        for other_rule, other_selector in css_rules:
            if rule != other_rule and selector in other_selector:
                cleaned.discard(other_rule)
    return list(cleaned)


def clean_adblock_rules_in_place(file_path):
    """清理 Adblock 规则并直接覆盖原文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        rules = [line.strip() for line in f if line.strip() and not line.startswith('!')]

    print(f"原始规则数: {len(rules)}")
    rules = remove_exact_duplicates(rules)
    print(f"移除完全重复规则后: {len(rules)}")

    grouped = group_rules(rules)

    # 处理域名规则
    domain_rules = grouped.get('domain', [])
    domain_rules = remove_subsumed_domain_rules(domain_rules)
    print(f"移除冗余域名规则后: {len(domain_rules)}")

    # 处理 CSS 规则
    css_rules = grouped.get('css', [])
    css_rules = remove_redundant_css_rules(css_rules)
    print(f"移除冗余 CSS 规则后: {len(css_rules)}")

    # 合并所有规则
    cleaned_rules = domain_rules + css_rules + grouped.get('generic', []) + grouped.get('exception', []) + grouped.get('exception_css', [])
    cleaned_rules = sorted(set(cleaned_rules))

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned_rules))

    print(f"清理后的规则已保存到原文件：{file_path}")


# 使用示例
file_path = './rules.txt'  # 输入规则文件路径
clean_adblock_rules_in_place(file_path)
