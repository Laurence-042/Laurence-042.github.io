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
    '<div class="flex flex-wrap nl3 nr3">',
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

    # 技术栈标签
    tag_html = ''.join(
        f'<span class="f7 dib bg-washed-blue br1 ph2 pv1 mr1 mb1 dark-blue">{t}</span>'
        for t in tech_stack
    )

    github_url = f"https://github.com/{repo}" if repo else ""
    demo_url   = f"/project/{project_id}/demo/"
    page_url   = f"/project/{project_id}/"

    card = f"""\
<div class="w-50-l w-100 ph3 mb4">
<div class="h-100 ba b--black-10 br2 pa4 flex flex-column">
<h3 class="f4 fw7 mt0 mb2"><a href="{page_url}" class="link dark-gray dim">{name}</a></h3>
<p class="f6 mid-gray mt0 mb3 flex-auto">{desc}</p>
{f'<div class="mb3">{tag_html}</div>' if tag_html else ''}\
{f'<p class="f7 mid-gray mt0 mb2 i">✨ {" · ".join(features)}</p>' if features else ''}\
<div class="flex items-center justify-between mt2">
{f'<a href="{github_url}" class="f7 link blue dim" target="_blank" rel="noopener">GitHub ↗</a>' if github_url else '<span></span>'}\
<a href="{demo_url}" class="f6 fw6 link white bg-dark-blue br1 pv2 ph3 dim no-underline">在线演示 →</a>
</div>
</div>
</div>"""

    lines.append(card)
    lines.append("")

lines.append("</div>")
lines.append("")

# 写入目标文件
out_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'project', '_index.md')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

log(f"已写入 {out_path}，共 {len(project_ids)} 个项目")
