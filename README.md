# 支付宝H5登录系统

基于FastAPI的支付宝OAuth授权登录系统，支持H5移动端登录，可部署在Render等云平台。

## 🚀 功能特性

- ✅ 支付宝OAuth 2.0授权登录
- ✅ H5移动端优化界面
- ✅ 用户信息获取和展示
- ✅ 访问令牌管理
- ✅ 支持沙箱和生产环境
- ✅ Docker容器化部署
- ✅ Render平台一键部署
- ✅ 完整的错误处理
- ✅ 响应式设计

## 📋 系统要求

- Python 3.11+
- 支付宝开放平台应用
- 域名（用于回调地址配置）

## 🛠️ 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd h5loginpython
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的支付宝应用配置：

```env
# 支付宝应用配置
ALIPAY_APP_ID=your_app_id_here
ALIPAY_APP_PRIVATE_KEY=your_app_private_key_here
ALIPAY_PUBLIC_KEY=your_alipay_public_key_here

# 网关地址（沙箱环境）
ALIPAY_GATEWAY_URL=https://openapi.alipaydev.com/gateway.do
ALIPAY_OAUTH_GATEWAY_URL=https://openauth.alipaydev.com/oauth2/publicAppAuthorize.htm
```

### 4. 启动应用

```bash
python main.py
```

或使用uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

访问 `http://localhost:8000` 查看登录页面。

## 🔧 支付宝开放平台配置

### 1. 创建应用

1. 登录 [支付宝开放平台](https://open.alipay.com/)
2. 进入开发者中心，创建「网页&移动应用」
3. 添加功能：「获取会员信息」

### 2. 配置密钥

1. 下载 [支付宝密钥生成工具](https://opendocs.alipay.com/common/02kipl)
2. 生成RSA2密钥对
3. 在应用中上传应用公钥
4. 获取支付宝公钥

### 3. 设置授权回调地址

在应用的「开发设置」中配置授权回调地址：

- 开发环境：`http://localhost:8000/auth/alipay/callback`
- 生产环境：`https://yourdomain.com/auth/alipay/callback`

## 📁 项目结构

```
h5loginpython/
├── main.py                 # FastAPI主应用
├── requirements.txt        # Python依赖
├── config/                 # 配置模块
│   ├── __init__.py
│   └── alipay_config.py   # 支付宝配置
├── services/              # 服务层
│   ├── __init__.py
│   └── alipay_service.py  # 支付宝服务
├── models/                # 数据模型
│   ├── __init__.py
│   └── user_models.py     # 用户模型
├── static/                # 静态文件
│   ├── login.html         # 登录页面
│   └── success.html       # 成功页面
├── .env.example           # 环境变量模板
├── .gitignore            # Git忽略文件
├── Dockerfile            # Docker配置
├── render.yaml           # Render部署配置
└── README.md             # 项目文档
```

## 🌐 API接口

### 授权登录

```
GET /auth/alipay
```

重定向到支付宝授权页面。

### 授权回调

```
GET /auth/alipay/callback?auth_code=xxx&state=xxx
```

处理支付宝授权回调，返回用户信息和访问令牌。

### 获取用户信息

```
GET /api/user/info?access_token=xxx
```

使用访问令牌获取用户信息。

### 健康检查

```
GET /health
```

检查服务状态。

## 🚀 部署指南

### Render部署

1. 将代码推送到GitHub
2. 在 [Render](https://render.com) 创建新的Web Service
3. 连接GitHub仓库
4. 配置环境变量：
   - `ALIPAY_APP_ID`
   - `ALIPAY_APP_PRIVATE_KEY`
   - `ALIPAY_PUBLIC_KEY`
5. 部署完成后更新支付宝应用的回调地址

### Docker部署

```bash
# 构建镜像
docker build -t alipay-h5-login .

# 运行容器
docker run -d \
  --name alipay-h5-login \
  -p 8000:8000 \
  -e ALIPAY_APP_ID=your_app_id \
  -e ALIPAY_APP_PRIVATE_KEY=your_private_key \
  -e ALIPAY_PUBLIC_KEY=your_public_key \
  alipay-h5-login
```

### 使用docker-compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ALIPAY_APP_ID=${ALIPAY_APP_ID}
      - ALIPAY_APP_PRIVATE_KEY=${ALIPAY_APP_PRIVATE_KEY}
      - ALIPAY_PUBLIC_KEY=${ALIPAY_PUBLIC_KEY}
    env_file:
      - .env
    restart: unless-stopped
```

启动：

```bash
docker-compose up -d
```

## 🔒 安全注意事项

1. **密钥安全**：
   - 私钥绝不能泄露
   - 生产环境使用环境变量存储敏感信息
   - 定期轮换密钥

2. **HTTPS**：
   - 生产环境必须使用HTTPS
   - 配置SSL证书

3. **域名验证**：
   - 回调地址必须与配置的域名一致
   - 验证state参数防止CSRF攻击

4. **令牌管理**：
   - 访问令牌有时效性
   - 及时刷新过期令牌
   - 安全存储用户令牌

## 🐛 常见问题

### Q: 授权失败，提示"应用未上线"

A: 确保支付宝应用已通过审核并上线，或使用沙箱环境进行测试。

### Q: 回调地址不匹配

A: 检查支付宝应用配置的授权回调地址是否与实际部署地址一致。

### Q: 签名验证失败

A: 检查应用私钥和支付宝公钥是否正确配置，注意密钥格式。

### Q: 获取用户信息失败

A: 确保访问令牌有效，检查授权范围是否包含用户信息权限。

## 📚 相关文档

- [支付宝开放平台文档](https://opendocs.alipay.com/)
- [用户信息授权](https://opendocs.alipay.com/open/263/105809)
- [OAuth 2.0授权](https://opendocs.alipay.com/open/220/105337)
- [Python SDK文档](https://opendocs.alipay.com/common/02np8q)
- [FastAPI文档](https://fastapi.tiangolo.com/)

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 📄 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 📞 支持

如果你在使用过程中遇到问题，可以：

1. 查看[常见问题](#-常见问题)部分
2. 提交[Issue](../../issues)
3. 参考支付宝开放平台文档

---

**注意**：本项目仅供学习和参考使用，生产环境使用请确保符合相关法律法规和支付宝开放平台的使用条款。