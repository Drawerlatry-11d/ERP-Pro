# ERP-Pro 部署说明（生产服务器）

> 适用范围：121.41.17.150（Ubuntu 22.04）。与现有 self-media（:80, 库 media_ops）完全隔离，互不影响。

## 1. 部署架构

```
浏览器 ──(8080)──> nginx (0.0.0.0:8080)
                      ├── /api/*  ──proxy──> gunicorn + Django (127.0.0.1:8000)
                      ├── /static/* ──alias──> /opt/erp/staticfiles/
                      └── /*        ──root───> /opt/erp/frontend/   (UI 原型占位)

Django ──PyMySQL──> MySQL 8 (库 erp / 用户 erp@localhost，与 media_ops 隔离)
```

要点：
- **后端只监听 127.0.0.1:8000**（仅本机），对外统一走 nginx 8080，避免直接暴露。
- **nginx 用 8080 而非 80**，因为 80 已被 self-media 的 node 占用。
- 复用系统 MySQL 实例，新建独立库 `erp` 与独立用户，权限隔离，不碰 `media_ops`。
- 当前未装 Redis：骨架阶段用 Django 本地缓存 + 数据库会话即可运行；待 P0 功能（异步导出/Celery）开发时再装。

## 2. 目录与服务

| 项 | 路径 |
| --- | --- |
| 项目代码 | `/opt/erp` |
| Python 虚拟环境 | `/opt/erp/venv` |
| 运行配置(.env) | `/opt/erp/.env`（含 DB/SECRET，权限 600，勿外泄） |
| 前端静态(占位) | `/opt/erp/frontend/` |
| 收集后的静态 | `/opt/erp/staticfiles/` |
| 后端 systemd | `/etc/systemd/system/erp-backend.service` |
| nginx 站点 | `/etc/nginx/sites-available/erp`（已软链到 sites-enabled） |

## 3. 常用运维

```bash
# 重启后端 / nginx
systemctl restart erp-backend
systemctl restart nginx

# 查看后端实时日志
journalctl -u erp-backend -f

# 数据库迁移 / 收集静态（先 cd /opt/erp）
venv/bin/python manage.py migrate
venv/bin/python manage.py collectstatic --noinput

# 创建/修改超级用户
venv/bin/python manage.py createsuperuser
```

## 4. 更新代码

由于该服务器到 GitHub 的 `git clone` 走 GnuTLS 会被中断，更新采用「本地改代码 → push GitHub → SFTP 上传到 /opt/erp（排除 .git）→ 重启」：

```bash
# 本地：把 ERP-Pro 源码（排除 .git / venv / __pycache__）同步到 /opt/erp
# 可用任意 SFTP 工具；同步后：
ssh root@121.41.17.150 'cd /opt/erp && venv/bin/python manage.py migrate && systemctl restart erp-backend'
```

> 也可在服务器用 `git pull`（若网络恢复），但当前以 SFTP 为稳妥路径。

## 5. 访问地址

- 前端：http://121.41.17.150:8080/
- API 文档（Swagger）：http://121.41.17.150:8080/api/docs/

⚠️ **必须在阿里云安全组放行 8080 端口入站**（TCP），否则公网无法访问。

## 6. 安全与凭据

- 数据库密码、Django `SECRET_KEY`、admin 密码均为部署时自动生成，保存在服务器 `/opt/erp/.env` 与本地 `~/erp_secrets.env`。
- **注意**：服务器 SSH root 密码（`Season69130`，首字母大写）与 MySQL root 密码（`season69130`，全小写）不同。
- 请勿将 `.env` 或含密码的文件提交到代码仓库或分享。
- 当前为「可运行底座」：后端骨架（模型/接口结构）已完成迁移；P0 业务功能尚未实现，前端为占位原型，待 UI 确认后进入正式开发。
