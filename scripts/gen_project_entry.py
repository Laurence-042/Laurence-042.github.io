"""
生成单个项目的 Markdown 卡片条目，追加到项目索引页面。
用法: python3 scripts/gen_project_entry.py <project_id>
"""
import yaml
import sys

project_id = sys.argv[1]

with open('projects.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# 合并顶层 projects 字典和可能误放在顶层的项目（YAML 格式宽容处理）
all_projects = dict(config.get('projects') or {})
for k, v in config.items():
    if k not in ('projects', 'global') and isinstance(v, dict) and 'name' in v:
        all_projects[k] = v

info = all_projects.get(project_id, {})

name       = info.get('name', project_id)
desc       = info.get('description', '')
repo       = info.get('repository', '')
tech_stack = info.get('tech_stack', [])
features   = info.get('features', [])

print(f"### [{name}](/project/{project_id}/)\n")
if desc:
    print(f"> {desc}\n")
if repo:
    print(f"🔗 **源码**: [github.com/{repo}](https://github.com/{repo})")
if tech_stack:
    print(f"🛠️ **技术栈**: {', '.join(tech_stack)}")
if features:
    print(f"✨ **特性**: {' · '.join(features)}")
print(f"\n**[在线演示 →](/project/{project_id}/demo/)**\n")
print("---\n")
