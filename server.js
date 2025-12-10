// server.js
require('dotenv').config();

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = process.env.PORT || 3000;

// ===== 中间件 =====
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态资源：把 ../public 当成前端目录
app.use(express.static(path.join(__dirname, '..', 'public')));

// ===== 简单健康检查 =====
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', time: new Date().toISOString() });
});

// ===== 联系我们表单接口 /api/contact =====
// 前端“留言咨询”表单走这里
app.post('/api/contact', (req, res) => {
  const { name, phone, email, subject, message } = req.body || {};

  if (!name || !email || !message) {
    return res.status(400).json({
      ok: false,
      error: '姓名、邮箱和留言内容为必填项'
    });
  }

  // 这里简单打印，你可以改成：
  // - 写数据库
  // - 发邮件到老师邮箱
  console.log('收到新的留言：', {
    name,
    phone,
    email,
    subject,
    message,
    time: new Date().toISOString()
  });

  return res.json({ ok: true });
});

// ===== 腾讯混元 AI 接口 /api/ai/chat =====

// 混元接口域名与路径（官方文档）:contentReference[oaicite:1]{index=1}
const HUNYUAN_ENDPOINT_HOST = 'hunyuan.cloud.tencent.com';
const HUNYUAN_ENDPOINT_PATH = '/hyllm/v1/chat/completions';

/**
 * 把 messages 数组转成签名需要的字符串形式
 * 例如: [{role:'user', content:'你好'}] -> [{"role":"user","content":"你好"}]
 * 注意要手动拼接，避免 JSON 库自动转义影响签名
 */
function buildMessagesString(messages = []) {
  const parts = messages.map((m) => {
    const role = String(m.role || '').replace(/"/g, '\\"');
    const content = String(m.content || '').replace(/"/g, '\\"');
    return `{"role":"${role}","content":"${content}"}`;
  });
  return `[${parts.join(',')}]`;
}

/**
 * 数字格式化：
 * - 整数保持不变
 * - 小数去掉无意义的 0 和最后的点号（比如 1.0 -> 1，0.80 -> 0.8）
 */
function formatNumber(n) {
  if (typeof n === 'number') {
    if (Number.isInteger(n)) return String(n);
    return String(n).replace(/0+$/, '').replace(/\.$/, '');
  }
  return String(n);
}

/**
 * 生成腾讯混元签名（HmacSHA1 + Base64）
 * 步骤（根据官方文档略化）:contentReference[oaicite:2]{index=2}
 * 1. 将所有参数按参数名字典序排序
 * 2. 拼接成 query 字符串：key=value&key2=value2...
 * 3. 前面加上域名和路径，组成 signStr:
 *    hunyuan.cloud.tencent.com/hyllm/v1/chat/completions? + query
 * 4. 使用 secretKey 做 HmacSHA1，再 Base64
 */
function genHunyuanSignature(params, secretKey) {
  const keys = Object.keys(params).sort();
  const query = keys
    .map((key) => {
      const value = params[key];
      if (typeof value === 'number') {
        return `${key}=${formatNumber(value)}`;
      }
      return `${key}=${value}`;
    })
    .join('&');

  const signStr = `${HUNYUAN_ENDPOINT_HOST}${HUNYUAN_ENDPOINT_PATH}?${query}`;
  const hmac = crypto.createHmac('sha1', secretKey);
  hmac.update(signStr, 'utf8');
  return hmac.digest('base64');
}

/**
 * /api/ai/chat
 * 请求体示例：
 * {
 *   "messages": [
 *     {"role": "user", "content": "请帮我介绍一下福州大学计算机与大数据学院"}
 *   ]
 * }
 */
app.post('/api/ai/chat', async (req, res) => {
  try {
    const userMessages = req.body.messages;

    if (!Array.isArray(userMessages) || userMessages.length === 0) {
      return res.status(400).json({ error: 'messages 必须是非空数组' });
    }

    const appId = process.env.HUNYUAN_APP_ID;
    const secretId = process.env.HUNYUAN_SECRET_ID;
    const secretKey = process.env.HUNYUAN_SECRET_KEY;

    if (!appId || !secretId || !secretKey) {
      return res.status(500).json({
        error: '后端未配置腾讯混元凭据，请在 .env 中设置 HUNYUAN_APP_ID / SECRET_ID / SECRET_KEY'
      });
    }

    const now = Math.floor(Date.now() / 1000);
    const expired = now + 60 * 5; // 签名 5 分钟内有效即可

    // 1. 构造签名所需参数（messages 用字符串）
    const messagesStr = buildMessagesString(userMessages);

    const signParams = {
      app_id: appId,
      expired,
      messages: messagesStr,
      secret_id: secretId,
      stream: 0,
      temperature: typeof req.body.temperature === 'number' ? req.body.temperature : 0.8,
      timestamp: now,
      top_p: typeof req.body.top_p === 'number' ? req.body.top_p : 0.8
    };

    if (req.body.query_id) {
      signParams.query_id = req.body.query_id;
    }

    // 2. 生成签名
    const signature = genHunyuanSignature(signParams, secretKey);

    // 3. 实际请求体（这里 messages 用正常 JSON 数组）
    const payload = {
      app_id: Number(appId),
      secret_id: secretId,
      timestamp: now,
      expired,
      stream: 0,
      temperature: signParams.temperature,
      top_p: signParams.top_p,
      messages: userMessages
    };

    if (signParams.query_id) {
      payload.query_id = signParams.query_id;
    }

    // 4. 调用腾讯混元接口
    const url = `https://${HUNYUAN_ENDPOINT_HOST}${HUNYUAN_ENDPOINT_PATH}`;

    const response = await axios.post(url, payload, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: signature
      },
      timeout: 25000
    });

    const data = response.data;

    if (data.error) {
      return res.status(500).json({
        error: data.error.message || '腾讯混元返回错误',
        code: data.error.code
      });
    }

    // 同步模式下结果在 choices[0].messages[0].content（根据官方文档）:contentReference[oaicite:3]{index=3}
    const replyText =
      data.choices?.[0]?.messages?.[0]?.content ||
      data.choices?.[0]?.delta?.content ||
      '';

    return res.json({
      reply: replyText,
      usage: data.usage,
      raw: data // 如果你嫌太大可以去掉
    });
  } catch (err) {
    console.error('调用腾讯混元失败：', err.response?.data || err.message);
    return res.status(500).json({
      error: '调用腾讯混元接口失败',
      detail: err.response?.data || err.message
    });
  }
});

// ===== 启动服务 =====
app.listen(PORT, () => {
  console.log(`Backend server is running at http://localhost:${PORT}`);
});
