/** Import koa-encrypted-session instead of koa-session */
const encryptedSession = require('koa-encrypted-session');
const Keygrip = require('keygrip');
const Koa = require('koa');
const app = new Koa();

/** Redefining Keygrip to use sha512 instead of sha1 */
app.keys = new Keygrip(['insert 64 random characters here', 'insert 64 others random characters here'], 'sha512');

const CONFIG = {
  key: 'koa:sess', /** (string) cookie key (default is koa:sess) */
  /** (number || 'session') maxAge in ms (default is 1 days) */
  /** 'session' will result in a cookie that expires when session/browser is closed */
  /** Warning: If a session cookie is stolen, this cookie will never expire */
  maxAge: 86400000,
  autoCommit: true, /** (boolean) automatically commit headers (default true) */
  overwrite: true, /** (boolean) can overwrite or not (default true) */
  httpOnly: true, /** (boolean) httpOnly or not (default true) */
  signed: true, /** (boolean) signed or not (default true) */
  rolling: false, /** (boolean) Force a session identifier cookie to be set on every response. The expiration is reset to the original maxAge, resetting the expiration countdown. (default is false) */
  renew: false, /** (boolean) renew session when session is nearly expired, so we can always keep user logged in. (default is false)*/

  /** koa-encrypted-session configuration */
  maxAge: 7 * 24 * 3600 * 1000,
  secret: 'insert 32 random characters here'
};

/**
This library inherits from koa-session, so all of its options can be used.
An additional mandatory secret options is introduced, which must be 256 Bits (32 characters) long.
By default, cookie signing is turned off, as AES256-GCM already takes care of this. */
app.use(encryptedSession(CONFIG, app));

app.use(ctx => {
  // ignore favicon
  if (ctx.path === '/favicon.ico') return;

  let n = ctx.session.views || 0;
  ctx.session.views = ++n;
  ctx.body = n + ' views';
  console.log(ctx.request.header.cookie);
});

app.listen(3001);
console.log('http://localhost:3001/');
