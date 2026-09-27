

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

```
1. 生成 16 字节随机数，用 bcrypt 专用的 Base64 编码成 22 个字符 -> salt
2. hash("123" + salt)  -> aY0HlLjFl0yGq...   （salt 作为输入参与运算）
3. 输出: $2b$12$ + salt + 哈希结果


$2b$12$0DDODP4KIGwKFbtJKW.Vn.aY0HlLjFl0yGqfM211BC0UZYEOFSF9m
└─┘ └┬┘ └─────────┬──────────┘└──────────────┬─────────────┘
 │   │            │                          │
 │   │            │                          └─ 31 字符：真正的密码哈希
 │   │            └─ 22 字符：随机 salt（明文）
 │   └─ cost 因子：12（表示迭代 2^12 = 4096 轮）
 └─ bcrypt 算法版本


 随机 16 字节 → 编码成 22 字符 salt → salt 和密码一起喂给 bcrypt 迭代 4096 轮 → 把"参数前缀 + salt + 结果"整串存库
简单理解
1. 先生成 22 个字符随机字符作为盐
2. hash('原始密码'+盐) 得到哈希值
3.盐+哈希值   得到最终哈希结果
```