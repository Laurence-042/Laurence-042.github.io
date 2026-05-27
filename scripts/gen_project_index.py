"""
生成项目索引页面 content/project/_index.md。
用法: python3 scripts/gen_project_index.py <project1> <project2> ...
输出写入 content/project/_index.md
"""
import yaml
import sys
import os
from datetime import datetime, timezone

def log(msg):
    print(f"[gen_project_index] {msg}", file=sys.stderr)

# 读取 projects.yaml
yaml_path = os.path.join(os.path.dirname(__file__), '..', 'projects.yaml')
with open(yaml_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

log(f"projects.yaml 顶层 keys: {list(config.keys())}")

# 合并顶层 projects 字典和可能误放在顶层的项目
all_projects = dict(config.get('projects') or {})
for k, v in config.items():
    if k not in ('projects', 'global') and isinstance(v, dict) and 'name' in v:
        log(f"顶层发现游离项目，合并: {k}")
        all_projects[k] = v

log(f"已知项目: {list(all_projects.keys())}")

project_ids = sys.argv[1:]
log(f"待生成项目: {project_ids}")

# 生成 front matter + 页头
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
lines = [
    "---",
    'title: "项目演示"',
    f"date: {now}",
    "draft: false",
    "---",
    "",
    "# 项目演示集合",
    "",
    "这里收集了我的各个项目的在线演示。",
    "",
    "## 可用项目",
    "",
]

# 为每个项目生成卡片
for project_id in project_ids:
    info = all_projects.get(project_id, {})
    log(f"{project_id}: info keys = {list(info.keys()) if info else '(无匹配)'}")

    name       = info.get('name', project_id)
    desc       = info.get('description', '')
    repo       = info.get('repository', '')
    tech_stack = info.get('tech_stack', [])
    features   = info.get('features', [])

    lines.append(f"### [{name}](/project/{project_id}/)")
    lines.append("")
    if desc:
        lines.append(f"> {desc}")
        lines.append("")
    if repo:
        lines.append(f"🔗 **源码**: [github.com/{repo}](https://github.com/{repo})")
    if tech_stack:
        lines.append(f"🛠️ **技术栈**: {', '.join(tech_stack)}")
    if features:
        lines.append(f"✨ **特性**: {' · '.join(features)}")
    lines.append("")
    lines.append(f"**[在线演示 →](/project/{project_id}/demo/)**")
    lines.append("")
    lines.append("---")
    lines.append("")

# 写入目标文件
out_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'project', '_index.md')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

log(f"已写入 {out_path}，共 {len(project_ids)} 个项目")
