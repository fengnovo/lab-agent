

```
cd backend
source .venv/bin/activate

pkill -f "uvicorn app.main:app"
pkill -f uvicorn

// 或者
lsof -i :8000
kill -9 <PID>

uvicorn app.main:app --reload
```

```
POST /api/auth/login
⬇️
验证用户名 + 密码
⬇️
生成 JWT Token
⬇️
返回 Token + 用户信息
⬇️
前端保存 Token
⬇️
请求携带 Token
⬇️
后端解析 Token并验证
⬇️
获得当前登录用户
```