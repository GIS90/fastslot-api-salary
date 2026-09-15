---
alwaysApply: true
scene: git_message
---

# Git 提交信息生成规则

## 核心原则

1. **简洁明了**：首行不超过 50 个字符，简要概括本次提交的核心改动
2. **规范格式**：严格遵循 `<type>(<scope>): <subject>` 格式
3. **中文描述**：subject 部分使用中文，方便团队沟通
4. **合理范围**：scope 使用小写英文，表示本次提交影响的模块/功能区域

## 提交类型（type）

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| **feat** | 新功能 | 新增用户可见的功能或特性 |
| **fix** | 修复 Bug | 修复线上或开发环境的 Bug |
| **docs** | 文档更新 | 仅修改 README、注释、API 文档等 |
| **style** | 代码格式 | 不影响代码逻辑的格式调整（空格、缩进、分号等） |
| **refactor** | 代码重构 | 既不修 Bug 也不加功能，只是优化代码结构 |
| **perf** | 性能优化 | 提升系统性能的改动 |
| **test** | 测试相关 | 添加或修改单元测试、集成测试 |
| **build** | 构建系统 | 修改构建工具、依赖版本、打包配置 |
| **ci** | CI/CD | 修改持续集成/部署配置（如 GitHub Actions） |
| **chore** | 杂项 | 其他不修改源码的改动（如 .gitignore 更新） |
| **revert** | 回滚 | 撤销之前的某次提交 |
| **format** | 代码格式化 | 使用格式化工具（如 Black、Prettier）统一代码风格 |

## 格式示例

### ✅ 正确示例

```markdown
feat(用户模块): 添加手机号登录功能
fix(支付): 修复微信支付回调签名验证失败的问题
docs: 更新 README 中的环境配置说明
style(前端): 统一组件缩进为 2 空格
refactor(数据库): 优化用户查询逻辑，减少冗余 JOIN
perf(API): 添加 Redis 缓存，减少数据库查询
test(订单): 添加订单状态流转的单元测试
build: 升级 fastapi 到 0.115.0
ci: 配置 GitHub Actions 自动化部署流程
chore: 更新 .gitignore 忽略 .env 文件
format(后端): 使用 Black 格式化所有 Python 文件
revert: 回滚 feat(用户模块) 的提交
```
