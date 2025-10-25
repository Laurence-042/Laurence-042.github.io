---
title: "言阅姬 - 敏感词检测工具"
date: '2025-10-25T11:35:00+08:00'
draft: false
featured_image: '/images/yanyueji-banner.jpg'
description: "基于拼音匹配的智能敏感词检测浏览器工具"
tags: ["JavaScript", "工具", "浏览器扩展", "文本处理"]
categories: ["项目展示"]
---

# 🖋️ 言阅姬 (YanYueJi)

> Steam好评率98%，全球首款「寻找对话中敏感词」的游戏《ウーマンコミュニケーション/ 女性交流》通关后做的小玩具

## 🚀 在线体验

<div style="text-align: center; margin: 2em 0;">
  <a href="/project/my-pen-is-broken/demo/" 
     style="display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 1.2em;">
    🎯 立即体验言阅姬
  </a>
</div>

## 📖 项目简介

言阅姬是一个基于拼音匹配的智能敏感词检测工具，支持两种使用模式：

### 🤖 自动检测版
- 加载后立即扫描整个页面
- 自动高亮所有检测到的敏感词
- 在控制台输出详细检测结果
- 适合快速扫描和批量检测

### 👆 手动点击版
- 需要点击文字才会检测该处的敏感词
- 显示敏感词的拼音信息
- 支持精确的逐个确认
- 适合细致的手动检查

## 🛠️ 技术特色

### 智能拼音匹配
使用 `pinyin` 库将中文转换为拼音进行模糊匹配，可以检测到：
- 同音词替换
- 拼音相近的词汇
- 各种谐音敏感词

### 高效DOM处理
- 遍历页面所有文本节点
- 智能跳过脚本和样式标签
- 实时替换匹配内容为高亮元素
- 不影响页面原有功能

### 浏览器书签集成
- 无需安装任何扩展
- 一键添加到浏览器书签
- 在任意网页上即点即用
- 支持所有主流浏览器

## 📊 项目统计

- ⭐ **GitHub Stars**: 持续增长中
- 🔧 **构建工具**: Webpack + Babel
- 📦 **包大小**: 高度优化的压缩版本
- 🌐 **浏览器支持**: Chrome, Firefox, Safari, Edge

## 🎯 使用场景

1. **内容审核**: 快速检测文章、评论中的敏感内容
2. **教育用途**: 帮助理解敏感词检测机制
3. **开发测试**: 验证内容过滤系统的效果
4. **学习研究**: 了解拼音匹配算法的实际应用

## 🔗 相关链接

- 📚 **源码仓库**: [GitHub - my-pen-is-broken](https://github.com/Laurence-042/my-pen-is-broken)
- 🎮 **灵感来源**: Steam游戏《ウーマンコミュニケーション/ 女性交流》
- 📖 **构建文档**: [BUILD_GUIDE.md](https://github.com/Laurence-042/my-pen-is-broken/blob/main/BUILD_GUIDE.md)
- 📄 **许可证**: MIT License

## ⚠️ 使用说明

1. **添加书签**: 访问[演示页面](/project/my-pen-is-broken/demo/)，右键点击书签链接选择"添加到书签"
2. **开始使用**: 在任意网页上点击书签即可启动检测
3. **查看结果**: 自动版会直接高亮显示，手动版需要点击文字
4. **控制台输出**: 按F12打开开发者工具查看详细检测信息

## 🤝 参与贡献

欢迎大家参与项目改进：

- 🐛 **报告Bug**: 在GitHub Issues中提交问题
- 💡 **功能建议**: 提出新的功能想法
- 🔧 **代码贡献**: 提交Pull Request
- 📖 **文档完善**: 改进项目文档

---

*注意: 本工具仅用于技术研究和教育目的，请合理使用。*