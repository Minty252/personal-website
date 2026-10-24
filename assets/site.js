// hofmannmoritz.com: mail links, the request form of the wedding section and the
// project carousel. No cookies, no tracking.
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

  // Carousel: native horizontal scrolling with snap points; the buttons and dots
  // only scroll it. Without the script it still scrolls by swipe or trackpad.
  document.querySelectorAll("[data-karussell]").forEach(function (box) {
    var track = box.querySelector(".pf-spur");
    var slides = Array.prototype.slice.call(track.children);
    var dots = box.querySelectorAll(".pf-punkte button");
    var current = function () {
      return Math.round(track.scrollLeft / track.clientWidth);
    };
    var go = function (i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: "smooth" });
    };
    box.querySelector(".pf-zurueck").addEventListener("click", function () { go(current() - 1); });
    box.querySelector(".pf-weiter").addEventListener("click", function () { go(current() + 1); });
    dots.forEach(function (dot, i) { dot.addEventListener("click", function () { go(i); }); });
    var mark = function () {
      var i = current();
      dots.forEach(function (dot, j) { dot.setAttribute("aria-current", i === j ? "true" : "false"); });
      box.querySelector(".pf-zurueck").disabled = i === 0;
      box.querySelector(".pf-weiter").disabled = i === slides.length - 1;
    };
    track.addEventListener("scroll", function () { window.requestAnimationFrame(mark); }, { passive: true });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") go(current() + 1);
      if (e.key === "ArrowLeft") go(current() - 1);
    });
    mark();
  });
})();
