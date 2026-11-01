# ERP-Pro

基于 Web 的企业 ERP 系统（进销存 + 财务 + 客户/供应商），后端使用 **Python + Django + Django REST Framework + MySQL**。

> 当前为 **项目骨架 / 一期 P0 脚手架**（UI 评审通过后进入功能开发）。

## 技术栈

| 层 | 方案 |
|----|------|
| 语言 | Python 3.11+ |
| Web 框架 | Django 4.2(LTS) + DRF |
| 数据库 | MySQL 8.0（InnoDB，utf8mb4） |
| 缓存 / 队列 | Redis + Celery（二期报表导出 / 定时任务） |
| 接口文档 | drf-spectacular（Swagger） |
| 部署 | Docker Compose / Nginx + Gunicorn |

## 模块划分

| 应用(app) | 内容 |
|-----------|------|
| `apps.system` | 用户、部门、角色、权限(RBAC)、操作日志 |
| `apps.master` | 商品/分类、计量单位、仓库、客户、供应商 |
| `apps.purchase` | 采购订单、采购入库、采购退货（P0） |
| `apps.sales` | 销售订单、销售出库、销售退货（P0） |
| `apps.inventory` | 实时库存、库存流水、盘点、调拨（P0，核心） |
| `apps.finance` | 应收/应付、收付款、资金账户（P1） |
| `apps.reports` | 经营看板、进销存汇总、利润分析（P1） |

## 快速开始

```bash
# 1. 创建并激活虚拟环境（推荐用 WorkBuddy managed Python 的 venv）
python -m venv venv && source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 准备数据库（任选其一）
#   方式 A：本地用 docker 起 MySQL + Redis
docker compose up -d
cp .env.example .env   # 已含 MySQL/Redis 默认连接

#   方式 B：不装 MySQL，用默认 SQLite 快速跑通（无需改配置）

# 4. 生成迁移并建表
python manage.py makemigrations
python manage.py migrate

# 5. 创建超级管理员
python manage.py createsuperuser

# 6. 启动开发服务
python manage.py runserver
```

- 管理后台：http://127.0.0.1:8000/admin/
- API 文档(Swagger)：http://127.0.0.1:8000/api/docs/
- 业务接口前缀：`/api/system/`、`/api/master/`、`/api/purchase/`、`/api/sales/`、`/api/inventory/`、`/api/finance/`、`/api/reports/`

## 关键设计

- **库存一致性（头号难点）**：所有库存变更都走 `apps/inventory/services.py` 的
  `change_stock()`，采用「数据库事务 + `SELECT ... FOR UPDATE` 行锁 + `inventory_transaction` 流水表」三件套，杜绝超卖与不一致。
- **软删除**：业务表统一继承 `apps/common/models.py` 的 `BaseModel`（`is_deleted` 标记）。
- **金额/数量精度**：金额 `DECIMAL(18,2)`、数量 `DECIMAL(18,4)`，避免浮点误差。
- **单据状态机**：采购/销售/盘点/调拨等单据统一用 `apps/common/constants.py` 的状态枚举（草稿/待审核/已审核/已作废），后续接入状态机统一管理流转。

## 目录结构

```
ERP-Pro/
├── config/            # Django 项目配置（settings/urls/wsgi/asgi）
├── apps/
│   ├── common/        # 公共基类（BaseModel、常量）
│   ├── system/        # 系统/权限
│   ├── master/        # 主数据
│   ├── purchase/      # 采购（P0）
│   ├── sales/         # 销售（P0）
│   ├── inventory/     # 库存（P0，核心）
│   ├── finance/       # 财务（P1）
│   └── reports/       # 报表（P1）
├── docker-compose.yml # MySQL + Redis
├── requirements.txt
└── manage.py
```

## 实施阶段

Phase 0 选型与环境 → Phase 1 基础框架与权限 → Phase 2 进销存核心闭环（P0）→
Phase 3 财务对接 → Phase 4 报表统计 → Phase 5 订单中心与审批流 → Phase 6 测试与上线。

详见项目资料库中的 `ERP系统开发规划.md`、`PRD_企业ERP系统_v1.md`、`评审结论_企业ERP系统_v1.md`。
