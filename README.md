# ReposBackup

> **备份 GitHub 仓库代码到多种云存储 / Back up GitHub repositories to cloud storage.**

[![GitHub Action](https://img.shields.io/badge/GitHub-Action-blue?logo=github)](https://github.com/bigbugcc/ReposBackup)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ 功能 Features

| 功能 | 说明 |
|------|------|
| ☁️ Cloudflare R2 | S3 兼容对象存储 |
| 🌤️ 腾讯云 COS | Tencent Cloud Object Storage |
| 🌥️ 阿里云 OSS | Alibaba Cloud Object Storage |
| 📂 FTP | 标准 FTP 服务器 |
| 📡 WebDAV | WebDAV 协议服务器 |
| 🏠 备份当前仓库 | 在当前仓库 Workflow 中调用 |
| 📦 批量备份 | 一次备份多个仓库 |
| 🌿 全量备份 | 备份所有分支 |
| 🎯 指定分支 | 只备份某个分支 |
| 📝 备份报告 | 自动生成 Markdown 备份报告 |

---

## 🚀 快速开始 Quick Start

### 备份当前仓库（单仓库模式）

在你的仓库中创建 `.github/workflows/backup.yml`：

```yaml
name: Backup Repository

on:
  schedule:
    - cron: "0 2 * * *"   # 每天 02:00 UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: bigbugcc/ReposBackup@main
        with:
          storage_type: r2             # 选择存储类型
          backup_branch: all           # all = 全部分支，或填写分支名

          # Cloudflare R2 凭据（存入仓库 Secrets）
          r2_account_id: ${{ secrets.R2_ACCOUNT_ID }}
          r2_access_key_id: ${{ secrets.R2_ACCESS_KEY_ID }}
          r2_secret_access_key: ${{ secrets.R2_SECRET_ACCESS_KEY }}
          r2_bucket_name: ${{ secrets.R2_BUCKET_NAME }}
```

### 批量备份多个仓库

```yaml
name: Batch Backup

on:
  schedule:
    - cron: "0 3 * * *"
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: bigbugcc/ReposBackup@main
        with:
          storage_type: r2
          backup_branch: all
          github_token: ${{ secrets.PAT_TOKEN }}   # 私有仓库需要 PAT

          # 每行一个仓库（owner/repo 格式）
          repos: |
            myorg/repo-one
            myorg/repo-two
            another-user/public-repo

          r2_account_id: ${{ secrets.R2_ACCOUNT_ID }}
          r2_access_key_id: ${{ secrets.R2_ACCESS_KEY_ID }}
          r2_secret_access_key: ${{ secrets.R2_SECRET_ACCESS_KEY }}
          r2_bucket_name: ${{ secrets.R2_BUCKET_NAME }}
```

---

## ⚙️ 输入参数 Inputs

### 通用参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `storage_type` | ✅ | — | 存储类型：`r2` / `tencent_cos` / `aliyun_oss` / `ftp` / `webdav` |
| `repos` | ❌ | _(当前仓库)_ | 多行仓库列表（`owner/repo`，每行一个）；留空则备份当前仓库 |
| `backup_branch` | ❌ | `all` | 备份分支：`all` 表示所有分支，或填写具体分支名 |
| `github_token` | ❌ | `${{ github.token }}` | 访问仓库的 GitHub Token（私有仓库需提供 PAT） |
| `generate_report` | ❌ | `true` | 是否在 Workflow 日志中输出 Markdown 备份报告 |

### ☁️ Cloudflare R2

| 参数 | 必填 | 说明 |
|------|------|------|
| `r2_account_id` | ✅ | Cloudflare 账户 ID |
| `r2_access_key_id` | ✅ | R2 API Token Access Key ID |
| `r2_secret_access_key` | ✅ | R2 API Token Secret Access Key |
| `r2_bucket_name` | ✅ | R2 存储桶名称 |
| `r2_bucket_path` | ❌ | 桶内路径前缀（可选） |

**获取凭据：** Cloudflare Dashboard → R2 → Manage R2 API Tokens

### 🌤️ 腾讯云 COS

| 参数 | 必填 | 说明 |
|------|------|------|
| `cos_secret_id` | ✅ | API 密钥 SecretId |
| `cos_secret_key` | ✅ | API 密钥 SecretKey |
| `cos_bucket_name` | ✅ | 存储桶名称（格式：`name-AppId`，如 `mybucket-1234567890`） |
| `cos_region` | ✅ | 地域（如 `ap-guangzhou`） |
| `cos_bucket_path` | ❌ | 桶内路径前缀（可选） |

**获取凭据：** 腾讯云控制台 → 访问管理 → API 密钥管理

### 🌥️ 阿里云 OSS

| 参数 | 必填 | 说明 |
|------|------|------|
| `oss_access_key_id` | ✅ | AccessKey ID |
| `oss_access_key_secret` | ✅ | AccessKey Secret |
| `oss_bucket_name` | ✅ | Bucket 名称 |
| `oss_endpoint` | ✅ | Endpoint（如 `oss-cn-hangzhou.aliyuncs.com`） |
| `oss_bucket_path` | ❌ | Bucket 内路径前缀（可选） |

**获取凭据：** 阿里云控制台 → RAM 访问控制 → 用户 → 创建 AccessKey

### 📂 FTP

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `ftp_host` | ✅ | — | FTP 服务器地址 |
| `ftp_port` | ❌ | `21` | FTP 端口 |
| `ftp_username` | ✅ | — | FTP 用户名 |
| `ftp_password` | ✅ | — | FTP 密码 |
| `ftp_path` | ❌ | `/` | 服务器上的基础路径 |

### 📡 WebDAV

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `webdav_url` | ✅ | — | WebDAV 服务器 URL（如 `https://dav.example.com`） |
| `webdav_username` | ✅ | — | 用户名 |
| `webdav_password` | ✅ | — | 密码 |
| `webdav_path` | ❌ | `/` | 服务器上的基础路径 |

---

## 📂 存储结构 Storage Layout

备份文件按以下路径存储（`bucket_path` 前缀可选）：

```
[bucket_path/]<owner>/<repo>/<owner>_<repo>_<branch>_<timestamp>.zip
```

**示例：**
```
bigbugcc/ReposBackup/bigbugcc_ReposBackup_main_20240115_120000.zip
bigbugcc/ReposBackup/bigbugcc_ReposBackup_dev_20240115_120000.zip
```

---

## 📝 备份报告 Backup Report

每次成功备份后，会在 Workflow 日志中打印如下 Markdown 报告：

```markdown
# 📦 Repository Backup Report

> Generated at: **2024-01-15 12:00:00 UTC**

## Summary

| Item             | Value             |
|------------------|-------------------|
| Storage Backend  | Cloudflare R2     |
| Backup Scope     | All branches      |
| Repositories     | 2                 |
| Archives Created | 4                 |
| Total Size       | 15.3 MB           |

## Backup Details

### 📁 `myorg/repo-one`

| Branch | Archive                                   | Size   |
|--------|-------------------------------------------|--------|
| `dev`  | `myorg_repo-one_dev_20240115_120000.zip`  | 3.2 MB |
| `main` | `myorg_repo-one_main_20240115_120000.zip` | 4.1 MB |
```

---

## 🔒 安全建议 Security

- 所有凭据请存入仓库的 **Secrets**（Settings → Secrets and variables → Actions），**切勿**写入 Workflow 文件明文。
- 批量备份私有仓库时，使用只有 `repo:read` 权限的最小化 PAT。
- 建议为云存储账号单独创建子账号并限制到目标 Bucket 的写权限。

---

## 🛠️ 本地开发 Local Development

```bash
# 克隆仓库
git clone https://github.com/bigbugcc/ReposBackup.git
cd ReposBackup

# 安装依赖
pip install -r requirements.txt

# 配置环境变量后运行
export STORAGE_TYPE=r2
export R2_ACCOUNT_ID=...
export GITHUB_REPOSITORY=owner/repo
python src/backup.py
```

### 项目结构

```
ReposBackup/
├── action.yml                          # GitHub Action 定义
├── requirements.txt                    # Python 依赖
├── src/
│   ├── backup.py                       # 主入口
│   ├── config.py                       # 配置加载
│   ├── git_utils.py                    # Git 克隆 / 打包工具
│   ├── report.py                       # Markdown 报告生成
│   └── storage/
│       ├── __init__.py                 # 存储工厂
│       ├── base.py                     # 抽象基类
│       ├── r2.py                       # Cloudflare R2
│       ├── cos.py                      # 腾讯云 COS
│       ├── oss.py                      # 阿里云 OSS
│       ├── ftp.py                      # FTP
│       └── webdav.py                   # WebDAV
└── .github/
    └── workflows/
        ├── backup-current.yml          # 备份当前仓库示例
        └── backup-batch.yml            # 批量备份示例
```

---

## 📄 License

MIT © [bigbugcc](https://github.com/bigbugcc)
