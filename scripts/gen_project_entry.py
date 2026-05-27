"""
生成单个项目的 Markdown 卡片条目，追加到项目索引页面。
用法: python3 scripts/gen_project_entry.py <project_id>
"""
import yaml
import sys

def log(msg):
    """调试日志输出到 stderr，不污染 stdout 的 Markdown 内容"""
    print(f"[gen_project_entry] {msg}", file=sys.stderr)

project_id = sys.argv[1]
log(f"处理项目: {project_id}")

with open('projects.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

log(f"projects.yaml 顶层 keys: {list(config.keys())}")

# 合并顶层 projects 字典和可能误放在顶层的项目（YAML 格式宽容处理）
all_projects = dict(config.get('projects') or {})
log(f"projects 下的项目: {list(all_projects.keys())}")

for k, v in config.items():
    if k not in ('projects', 'global') and isinstance(v, dict) and 'name' in v:
        log(f"顶层发现游离项目，合并: {k}")
        all_projects[k] = v

info = all_projects.get(project_id, {})
log(f"匹配到的 info keys: {list(info.keys()) if info else '(无匹配)'}")

name       = info.get('name', project_id)
desc       = info.get('description', '')
repo       = info.get('repository', '')
tech_stack = info.get('tech_stack', [])
features   = info.get('features', [])

log(f"name={name!r}  desc={desc!r}  repo={repo!r}  tech={tech_stack}  features={features}")

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
log("完成")
