// =============================================
// お問い合わせフォームの受け口
//
// 送信は母屋（IFS-Manager / IFHR / IF-Shopify）と同じ形。
// nodemailer + Google Workspace の SMTP（アプリパスワード）。
//
// 【絶対】鍵をこのファイルに書かないこと。このリポジトリは公開されている。
// 値は Vercel の環境変数に入れる（松井が入れる）:
//   SMTP_USER     送信に使うアカウント（例: matsui@inspherefarm.com）
//   SMTP_PASS     アプリパスワード16桁
//   SMTP_HOST     省略可（既定 smtp.gmail.com）
//   SMTP_PORT     省略可（既定 465）
//   SMTP_SECURE   省略可（既定 true。587 を使うときだけ 'false'）
//   CONTACT_TO    省略可（既定 info@condorcet.jp）
//   CONTACT_FROM  省略可（既定 SMTP_USER。差出人を変えたいときだけ）
// =============================================
const nodemailer = require('nodemailer')

// 長すぎる入力は切る。嫌がらせで巨大な本文を送られても落ちないように
const MAX = { name: 100, company: 100, email: 200, tel: 50, body: 4000 }

function clean(v, max) {
  return String(v == null ? '' : v)
    .replace(/\r\n/g, '\n')
    .trim()
    .slice(0, max)
}

// 画面から来た人には、JavaScript が無くても結果が分かるページを返す
function htmlPage(title, message) {
  return `<!doctype html><html lang="ja"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>${title} — Condorcet</title>
<style>
:root{color-scheme:light}
body{margin:0;min-height:100svh;display:flex;align-items:center;justify-content:center;
background:#0f1f3d;color:#fff;font-family:'Hiragino Sans','Yu Gothic',Meiryo,sans-serif;padding:24px}
.w{max-width:32em;line-height:1.9}
h1{font-family:'Zen Old Mincho',serif;font-size:1.5rem;line-height:1.5;margin:0 0 .8em}
a{color:#8fb3ff}
</style>
<div class="w"><h1>${title}</h1><p>${message}</p><p><a href="/d/">ホームへ戻る</a></p></div>`
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST')
    return res.status(405).json({ ok: false })
  }

  const b = (req.body && typeof req.body === 'object') ? req.body : {}
  // JavaScript から来たか、素のフォーム送信で来たか
  const wantsHtml = !String(req.headers['content-type'] || '').includes('application/json')

  // --- 自動送信よけ ---------------------------------------------------
  // ① 画面に出ない欄が埋まっている ② 開いた直後（3秒未満）に送信された
  // どちらも人ではないので、黙って捨てる（捨てたことは相手に教えない）
  const opened = Number(b.t || 0)
  const tooFast = opened > 0 && Date.now() - opened < 3000
  if (clean(b.website, 200) || tooFast) {
    return wantsHtml
      ? res.status(200).send(htmlPage('送信しました', '2営業日以内にお返事します。'))
      : res.status(200).json({ ok: true })
  }

  // --- 中身の確認 -----------------------------------------------------
  const f = {
    name: clean(b.name, MAX.name),
    company: clean(b.company, MAX.company),
    email: clean(b.email, MAX.email),
    tel: clean(b.tel, MAX.tel),
    body: clean(b.body, MAX.body),
  }
  const okEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email)
  if (!f.name || !f.company || !okEmail || !f.body) {
    return wantsHtml
      ? res.status(400).send(htmlPage('入力に足りないところがあります',
          'お名前・会社名・メールアドレス・ご用件をご確認のうえ、もう一度お試しください。'))
      : res.status(400).json({ ok: false, error: 'invalid' })
  }

  const user = process.env.SMTP_USER
  const pass = process.env.SMTP_PASS
  if (!user || !pass) {
    console.error('SMTP_USER / SMTP_PASS が未設定です（Vercel の環境変数を確認）')
    return wantsHtml
      ? res.status(500).send(htmlPage('うまく送れませんでした',
          'お手数ですが、時間をおいてもう一度お試しください。'))
      : res.status(500).json({ ok: false })
  }

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port: Number(process.env.SMTP_PORT || 465),
    secure: (process.env.SMTP_SECURE || 'true') !== 'false',
    auth: { user, pass },
  })

  const text = [
    `お名前　： ${f.name}`,
    `会社名　： ${f.company}`,
    `メール　： ${f.email}`,
    `電話　　： ${f.tel || '（未記入）'}`,
    '',
    '── ご用件 ──',
    f.body,
    '',
    '──────────────',
    'condorcet.jp のお問い合わせフォームから届きました。',
    'このメールにそのまま返信すると、お客様に届きます。',
  ].join('\n')

  try {
    await transporter.sendMail({
      from: process.env.CONTACT_FROM || `Condorcet お問い合わせ <${user}>`,
      to: process.env.CONTACT_TO || 'info@condorcet.jp',
      // 返信すれば、そのままお客様に届く
      replyTo: `${f.name} <${f.email}>`,
      subject: `【お問い合わせ】${f.company}　${f.name} 様`,
      text,
    })
  } catch (e) {
    console.error('送信に失敗:', (e && e.message) || e)
    return wantsHtml
      ? res.status(502).send(htmlPage('うまく送れませんでした',
          'お手数ですが、時間をおいてもう一度お試しください。'))
      : res.status(502).json({ ok: false })
  }

  return wantsHtml
    ? res.status(200).send(htmlPage('送信しました', '2営業日以内にお返事します。'))
    : res.status(200).json({ ok: true })
}
