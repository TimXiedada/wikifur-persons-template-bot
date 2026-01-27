# WikiFur Persons Template Bot

一个自动生成和更新 WikiFur 人物导航模板的 Python 脚本。

## 概述

此项目自动从 WikiFur 的“人物”分类获取所有人物页面，将中文/日文名称转换为拼音/罗马字以便按字母排序，并生成符合 WikiFur 格式要求的导航模板（`模板:人物`）。脚本可以输出到控制台或直接推送到 WikiFur。

## 功能特性

- **自动获取页面**：从“人物”和“逝世的人物”分类获取所有页面
- **智能拼音转换**：支持中文汉字转拼音，日文假名转罗马字
- **自动分组排序**：按首字母分组（A·B·C·D, E·F·G·H, ..., #）
- **用户页面处理**：正确格式化用户命名空间页面（`[[用户:Name|Name]]`）
- **逝世标记**：为逝世人物添加 `{{Departed|...}}` 模板
- **安全推送**：仅当内容变化时更新，支持编辑冲突重试
- **多种运行模式**：输出到控制台、显示差异（dry-run）、直接推送
- **完整测试套件**：包含单元测试确保转换正确性

## 安装

### 环境要求

- Python 3.8+
- 依赖包：`mwclient`, `pypinyin`

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/wikifur-persons-template-bot.git
   cd wikifur-persons-template-bot
   ```

2. 安装依赖：
   ```bash
   pip install mwclient pypinyin
   ```

3. 配置 WikiFur 凭证（见下方配置部分）

## 配置

创建 `config.ini` 文件（已忽略于版本控制）：

```ini
[Location]
domain=zh.wikifur.com

[Credential]
username=你的用户名
password=你的密码
```

**警告**：不要将 `config.ini` 提交到版本控制！

## 使用方法

### 基本用法

```bash
# 生成模板并输出到控制台
python __main__.py

# 生成模板并直接推送到 WikiFur
python __main__.py --send

# 推送到指定页面
python __main__.py --send --page "模板:测试" --summary "测试更新"
```

### 高级选项

```bash
# 显示与当前页面内容的差异但不推送（dry-run）
python __main__.py --dry-run

# 显示详细日志
python __main__.py --verbose

# 只显示错误日志
python __main__.py --quiet

# 查看所有选项
python __main__.py --help
```

### 命令行选项

| 选项 | 缩写 | 描述 |
|------|------|------|
| `--send` | | 推送模板到 WikiFur（默认为仅输出到 stdout） |
| `--dry-run` | | 显示与当前页面内容的差异但不推送 |
| `--verbose` | `-v` | 显示详细日志 |
| `--quiet` | `-q` | 只显示错误日志 |
| `--page` | | 目标页面标题（默认为"模板:人物"） |
| `--summary` | | 编辑摘要（默认为自动生成） |
| `--help` | `-h` | 显示帮助信息 |

## 开发

### 项目结构

```
wikifur-persons-template-bot/
├── __main__.py          # 命令行入口点
├── convert.py           # 核心转换和模板生成
├── get.py               # Wiki 页面获取
├── send.py              # Wiki 页面更新
├── config.ini           # Wiki 凭证（本地文件，不提交）
├── tests/               # 单元测试
│   └── test_convert.py  # 转换逻辑测试
└── README.md            # 本文档
```

### 运行测试

```bash
# 安装测试依赖（如果需要）
pip install pytest

# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_convert.py::TestKanaToRomaji -v
```

### 代码规范

项目使用标准 Python 代码风格（PEP 8）。主要约定：

- 使用类型提示（Type Hints）
- 函数和类有文档字符串
- 使用 logging 模块而非 print 语句
- 关键函数有单元测试

## 工作原理

1. **获取页面列表**：通过 mwclient 从 WikiFur 获取“人物”和“逝世的人物”分类中的所有页面
2. **拼音转换**：使用 pypinyin 将中文转换为拼音，自定义函数处理日文假名
3. **排序分组**：按拼音首字母排序，分组成标准字母组
4. **模板生成**：生成符合 WikiFur 格式的 Navbox 模板
5. **推送更新**：比较当前页面内容，仅当有变化时更新

### 假名转换处理

由于 pypinyin 无法处理日文假名，脚本包含自定义的假名到罗马字转换表，覆盖：
- 所有平假名和片假名
- 拗音（きゃ、しゅ等）
- 特殊片假名组合（ヴァ、ファ、ティ等）

## 常见问题

### 编辑冲突处理

脚本使用指数退避策略处理编辑冲突：第一次冲突等待 2 秒，第二次 4 秒，第三次 8 秒，最多重试 3 次。

### 页面过滤规则

- 跳过子页面（标题中包含 "/" 的页面）
- 只处理主命名空间（0）和用户命名空间（2）的页面

### 性能考虑

脚本一次性获取所有页面，对于大型 Wiki 可能需要较长时间。建议定期运行（如每周一次）。

## 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 致谢

- [mwclient](https://github.com/mwclient/mwclient) - MediaWiki API 客户端
- [pypinyin](https://github.com/mozillazg/python-pinyin) - 汉字转拼音库
- WikiFur 社区提供的数据和平台支持