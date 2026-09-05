(function () {
  "use strict";

  document.documentElement.classList.add("is-ready");

  /* ============ WORD REVEAL: split .reveal-write into spans ============ */
  function wrapWords(root) {
    var counter = { i: 0 };

    function walk(node) {
      var children = Array.prototype.slice.call(node.childNodes);
      children.forEach(function (child) {
        if (child.nodeType === Node.TEXT_NODE) {
          var text = child.textContent;
          if (!text || !text.trim()) return;
          var frag = document.createDocumentFragment();
          // Split on whitespace but keep the whitespace as separate text nodes
          var parts = text.split(/(\s+)/);
          parts.forEach(function (part) {
            if (part === "") return;
            if (/^\s+$/.test(part)) {
              frag.appendChild(document.createTextNode(part));
            } else {
              var span = document.createElement("span");
              span.className = "reveal-word";
              span.style.setProperty("--word-index", counter.i);
              span.textContent = part;
              counter.i += 1;
              frag.appendChild(span);
            }
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === Node.ELEMENT_NODE) {
          walk(child);
        }
      });
    }

    walk(root);
  }

  var writeEls = document.querySelectorAll(".reveal-write");
  writeEls.forEach(function (el) {
    wrapWords(el);
  });

  /* ============ SCROLL REVEAL (IntersectionObserver) ============ */
  var revealSelectors = ".reveal-media, .reveal-side, .reveal-up, .reveal-mark, .reveal-write";
  var revealTargets = Array.prototype.slice.call(document.querySelectorAll(revealSelectors));

  function revealElement(el) {
    el.classList.add("is-visible");
    if (el.classList.contains("reveal-write")) {
      var words = el.querySelectorAll(".reveal-word");
      words.forEach(function (w) {
        w.classList.add("is-visible");
      });
    }
  }

  if ("IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            revealElement(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.22, rootMargin: "0px 0px -8% 0px" }
    );

    revealTargets.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealTargets.forEach(revealElement);
  }

  /* ============ HERO VIDEO AUTOPLAY RESILIENCE ============ */
  var heroVideos = Array.prototype.slice.call(document.querySelectorAll(".hero__video"));

  heroVideos.forEach(function (video) {
    video.muted = true;
    video.defaultMuted = true;
    video.autoplay = true;
    video.loop = true;
    video.playsInline = true;
    video.controls = false;
    video.disablePictureInPicture = true;
    video.disableRemotePlayback = true;

    var attempts = 0;
    var maxAttempts = 20;
    var settled = false;

    function tryPlay() {
      if (settled) return;
      attempts += 1;
      var playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise
          .then(function () {
            settled = true;
          })
          .catch(function () {
            if (attempts >= maxAttempts) {
              settled = true;
            }
          });
      }
    }

    video.addEventListener("loadeddata", tryPlay);
    video.addEventListener("pause", tryPlay);
    video.addEventListener("ended", tryPlay);

    document.addEventListener("visibilitychange", function () {
      if (!document.hidden) tryPlay();
    });
    window.addEventListener("pageshow", tryPlay);
    window.addEventListener("focus", tryPlay);
    window.addEventListener("touchstart", tryPlay, { passive: true });
    window.addEventListener("touchend", tryPlay, { passive: true });
    window.addEventListener("click", tryPlay);

    var retryInterval = setInterval(function () {
      if (settled || attempts >= maxAttempts) {
        clearInterval(retryInterval);
        return;
      }
      tryPlay();
    }, 1200);

    tryPlay();
  });

  /* ============ FAQ ACCORDION ============ */
  var faqItems = Array.prototype.slice.call(document.querySelectorAll(".faq-item"));

  faqItems.forEach(function (item) {
    var trigger = item.querySelector(".faq-item__trigger");
    var answer = item.querySelector(".faq-item__answer");

    trigger.addEventListener("click", function () {
      var isOpen = trigger.getAttribute("aria-expanded") === "true";

      faqItems.forEach(function (other) {
        var otherTrigger = other.querySelector(".faq-item__trigger");
        var otherAnswer = other.querySelector(".faq-item__answer");
        otherTrigger.setAttribute("aria-expanded", "false");
        otherAnswer.hidden = true;
      });

      if (!isOpen) {
        trigger.setAttribute("aria-expanded", "true");
        answer.hidden = false;
      }
    });
  });
})();


/* ============ ORÇAMENTO FORM (dobra visível) → WHATSAPP ============ */
(function () {
  "use strict";

  var WHATSAPP_NUMBER = "558396243847";
  var form = document.getElementById("quote-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var data = new FormData(form);
    var nome = (data.get("nome") || "").toString().trim();
    var nicho = (data.get("nicho") || "").toString().trim();
    var necessidade = (data.get("necessidade") || "").toString().trim();
    var tipo = (data.get("tipo") || "").toString().trim();
    var investimento = (data.get("investimento") || "").toString().trim();
    var manutencao = (data.get("manutencao") || "").toString().trim();
    var detalhes = (data.get("detalhes") || "").toString().trim();

    var lines = [
      "Olá, Igor. Tenho interesse em criar um site.",
      "",
      "Nome: " + nome,
      "Nicho: " + nicho,
      "Tipo de site: " + tipo,
      "Necessidade: " + necessidade,
      "Investimento pretendido: " + investimento
    ];
    if (manutencao) lines.push("Manutenção mensal: " + manutencao);
    if (detalhes) lines.push("Detalhes: " + detalhes);

    var message = lines.join("\n");
    var url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(message);
    window.open(url, "_blank", "noopener");
  });
})();
