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
    domain_rules = [rule for rule, _ in remove_subsumed_domain_rules(domain_rules)]
    print(f"移除冗余域名规则后: {len(domain_rules)}")

    # 处理 CSS 规则
    css_rules = grouped.get('css', [])
    css_rules = [rule for rule, _ in remove_redundant_css_rules(css_rules)]
    print(f"移除冗余 CSS 规则后: {len(css_rules)}")

    # 合并所有规则
    generic_rules = grouped.get('generic', [])
    exception_rules = grouped.get('exception', [])
    exception_css_rules = grouped.get('exception_css', [])

    cleaned_rules = (
        domain_rules +
        css_rules +
        generic_rules +
        exception_rules +
        exception_css_rules
    )

    # 确保所有规则是字符串类型，并排序
    cleaned_rules = sorted(set(cleaned_rules))

    # 写回原文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(cleaned_rules))

    # 输出处理后的完整文件内容
    print("\n清理后的完整规则文件内容:")
    print("\n".join(cleaned_rules))


# 使用示例
file_path = './rules.txt'  # 输入规则文件路径
clean_adblock_rules_in_place(file_path)
