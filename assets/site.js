// hofmannmoritz.com: mail links, the request form of the wedding section and the
// project tabs. No cookies, no tracking.
(function () {
  var en = document.documentElement.lang === "en";

  // The address is written backwards and base64-encoded in the HTML (same as on
  // fastpal.com), so address collectors that search the page text find nothing.
  var MAIL = "bW9jLnp0aXJvbW5uYW1mb2hAZW0=";
  var address = atob(MAIL).split("").reverse().join("");
  document.querySelectorAll("[data-mail]").forEach(function (a) {
    a.href = "mailto:" + address;
    if (!a.hasAttribute("data-mail-label")) a.textContent = address;
  });

  // Wedding request: the mail endpoint on fastpal.com, the same one /hochzeit used.
  var TEXT = en
    ? { sending: "Sending …", send: "Send request", thanks: "Thank you!", done: "Your request has arrived. I will reply on WhatsApp within the next few days.", fail: "Sending does not work right now.", write: "Write to me directly at" }
    : { sending: "Wird gesendet …", send: "Anfrage senden", thanks: "Danke!", done: "Eure Anfrage ist angekommen. Ich melde mich in den nächsten Tagen per WhatsApp.", fail: "Senden geht gerade nicht.", write: "Schreibt mir gern direkt an" };
  document.querySelectorAll("form[data-anfrage]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var button = form.querySelector("button[type=submit]");
      var old = form.querySelector(".hz-form-fehler");
      if (old) old.remove();
      button.disabled = true;
      button.textContent = TEXT.sending;
      var data = Object.fromEntries(new FormData(form));
      data.art = form.getAttribute("data-anfrage");
      data.sprache = en ? "en" : "de";
      // text/plain keeps it a simple request (no preflight); the route reads JSON anyway.
      fetch("https://fastpal.com/api/anfrage", { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(data) })
        .then(function (res) { return res.json().then(function (body) { return { ok: res.ok && body.ok, body: body }; }); })
        .catch(function () { return { ok: false, body: null }; })
        .then(function (r) {
          if (r.ok) {
            var done = document.createElement("div");
            done.className = "hz-form-danke";
            done.setAttribute("role", "status");
            done.innerHTML = '<p class="hz-betrag"></p><p></p>';
            done.children[0].textContent = TEXT.thanks;
            done.children[1].textContent = TEXT.done;
            form.replaceWith(done);
            return;
          }
          button.disabled = false;
          button.textContent = TEXT.send;
          var p = document.createElement("p");
          p.className = "hz-form-fehler";
          p.setAttribute("role", "alert");
          p.textContent = ((r.body && r.body.fehler) || TEXT.fail) + " " + TEXT.write + " ";
          var a = document.createElement("a");
          a.href = "mailto:" + address;
          a.textContent = address;
          p.append(a, ".");
          button.after(p);
        });
    });
  });

  // Projects: tabs switch the visible project. Without the script every project shows
  // one below the other (no hidden attributes in the HTML).
  document.querySelectorAll("[data-reiter]").forEach(function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll("[role=tab]"));
    var panels = tabs.map(function (tab) { return document.getElementById(tab.getAttribute("aria-controls")); });
    box.classList.add("pf-js");
    var show = function (i, focus) {
      tabs.forEach(function (tab, j) {
        var on = i === j;
        tab.setAttribute("aria-selected", on ? "true" : "false");
        tab.tabIndex = on ? 0 : -1;
        panels[j].hidden = !on;
      });
      if (focus) tabs[i].focus({ preventScroll: true });
      // Only the tab row scrolls (narrow screens), never the page.
      var list = tabs[i].parentElement;
      list.scrollLeft = Math.max(0, tabs[i].offsetLeft - list.offsetLeft - (list.clientWidth - tabs[i].offsetWidth) / 2);
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { show(i, false); });
      tab.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") show((i + 1) % tabs.length, true);
        if (e.key === "ArrowLeft") show((i - 1 + tabs.length) % tabs.length, true);
      });
    });
    show(0, false);
  });
})();
