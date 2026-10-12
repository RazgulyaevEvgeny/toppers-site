/* Заявки с сайта топперов -> учёт заказов студии (Firebase raz-studio).
   Когда клиент нажимает «Отправить заказ в WhatsApp», заявка параллельно
   записывается в базу учёта, а в текст сообщения добавляется её номер.
   Сайт может только создать новую заявку: читать и менять их могут
   только сотрудники (см. firestore.rules в репозитории raz-studio-crm). */
(function () {
  var FB = { project: "raz-studio-5a486", key: "AIzaSyCNpsnF-9swN11uS2L22-w9cXF45G54Hj0" };
  var ABC = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  function newCode() {
    var s = "T", a = new Uint32Array(6);
    (window.crypto || window.msCrypto).getRandomValues(a);
    for (var i = 0; i < 6; i++) s += ABC[a[i] % ABC.length];
    return s;
  }
  var code = newCode(), sentSig = null;

  function ready() { return typeof msg === "function" && typeof lines === "function" && typeof MODELS !== "undefined"; }
  function val(id) { var el = document.getElementById(id); return el ? String(el.value || "").trim() : ""; }

  function collect() {
    var L = lines(), items = [], tot = 0, qty = 0, hasCustom = false;
    MODELS.forEach(function (m) {
      var ls = L.filter(function (l) { return l.m.id === m.id; });
      if (!ls.length) return;
      var T = total(m.id), u = m.noPrice ? 0 : unit(m, T);
      if (m.noPrice) hasCustom = true; else tot += u * T;
      qty += T;
      items.push({
        modelId: String(m.id), model: String(m.name), qty: T, price: u, sum: u * T,
        colors: m.custom ? [] : ls.map(function (l) { var c = colorsOf(m)[l.ci] || {}; return { name: String(c.n || ""), hex: String(c.c || ""), qty: l.q }; })
      });
    });
    return { items: items, total: tot, qty: qty, hasCustom: hasCustom };
  }

  /* номер заявки в тексте сообщения WhatsApp */
  var baseMsg = msg;
  function sig() { return baseMsg(); }
  window.msg = msg = function () {
    var s = baseMsg();
    if (sentSig !== null && s !== sentSig) { code = newCode(); sentSig = null; }
    return s + "\nНомер заявки: " + code;
  };

  /* перевод в формат Firestore REST */
  function fv(v) {
    if (v === null || v === undefined) return { nullValue: null };
    if (typeof v === "boolean") return { booleanValue: v };
    if (typeof v === "number") return Number.isInteger(v) ? { integerValue: String(v) } : { doubleValue: v };
    if (typeof v === "string") return { stringValue: v };
    if (Array.isArray(v)) return { arrayValue: { values: v.map(fv) } };
    var f = {}; Object.keys(v).forEach(function (k) { f[k] = fv(v[k]); }); return { mapValue: { fields: f } };
  }

  function send() {
    var c = collect();
    if (!c.items.length) return;
    var s = sig();
    if (sentSig === s) return;           // этот же заказ уже отправлен
    var doc = {
      source: "toppers", code: code, status: "new", createdAt: Date.now(),
      name: val("who").slice(0, 200), cafe: val("cafe").slice(0, 200), note: val("note").slice(0, 2000),
      customDesc: c.hasCustom ? val("cdesc").slice(0, 2000) : "",
      items: c.items.slice(0, 40), total: Math.round(c.total), qty: c.qty, hasCustom: c.hasCustom,
      text: (s + "\nНомер заявки: " + code).slice(0, 6000)
    };
    var url = "https://firestore.googleapis.com/v1/projects/" + FB.project + "/databases/(default)/documents/requests?documentId=" + code + "&key=" + FB.key;
    try {
      fetch(url, { method: "POST", keepalive: true, headers: { "Content-Type": "application/json" }, body: JSON.stringify({ fields: fv(doc).mapValue.fields }) })
        .catch(function () {});
    } catch (e) {}
    sentSig = s;
  }

  function boot() {
    if (!ready()) return setTimeout(boot, 200);
    var wa = document.getElementById("wa");
    if (!wa) return;
    wa.addEventListener("click", function () {
      if (wa.classList.contains("off") || wa.getAttribute("href") === "#") return;
      send();
    }, true);
    if (typeof render === "function") render();   // обновить ссылку WhatsApp с номером заявки
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
