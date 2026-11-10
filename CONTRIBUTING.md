# 贡献说明

本仓库署名 geniusjia666。许可证使用根目录现有的 MIT License，请保持该文件原样。

方法内容是中文 Skill。英文完整版在 <https://github.com/geniusjia666/agent-system-design>。两边的关系、版本号和手动同步流程见 [SYNC.md](SYNC.md)。

## 提出改动

用新分支和 PR 提交。不要在这个流程里打 tag 或创建 GitHub Release。PR 说明用中文，写清改动目的和你实际跑过的检查。

`skills/agent-system-design-cn/` 里的 14 个原始文件按字节保留。不要为了排版、译名或链接文字去改它们。若相对链接确实失效、必须修改，在 PR 中单独列出文件、原因和哈希变化。不要从英文仓库整份复制 Skill 来覆盖中文原文。

新增说明、示例和脚本使用中文。示例要标明哪些是推演、哪些做过运行。没有做宿主安装或框架安装时，不要写已验证、已兼容或已测试。

## 不要提交的内容

- 密钥、令牌、口令和私有配置
- 本机绝对路径、内部工作目录
- 压缩包带入的 macOS 资源分叉目录、AppleDouble 文件和桌面服务文件
- 可执行的框架示例依赖。参考文里的脚手架只作阅读，不要在贡献检查里运行它

## 提交前

在仓库根目录运行：

```bash
python3 scripts/validate_publication.py
```

脚本只用 Python 标准库。它检查 UTF-8、JSON、本地 Markdown 链接、`SKILL.md` frontmatter，以及原始文件的 SHA-256。它不安装依赖，也不执行 Skill 里的框架示例。
