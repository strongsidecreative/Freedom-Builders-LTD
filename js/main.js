/* Freedom Builders Ltd — site scripts */
(function () {
  "use strict";

  document.getElementById("year") &&
    (document.getElementById("year").textContent = new Date().getFullYear());

  /* ---------- header scroll state ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- mobile nav ---------- */
  var burger = document.querySelector(".hamburger");
  var mobileNav = document.querySelector(".mobile-nav");
  if (burger && mobileNav) {
    burger.addEventListener("click", function () {
      var open = burger.getAttribute("aria-expanded") === "true";
      burger.setAttribute("aria-expanded", String(!open));
      mobileNav.classList.toggle("is-open", !open);
      document.body.style.overflow = !open ? "hidden" : "";
    });
    mobileNav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        burger.setAttribute("aria-expanded", "false");
        mobileNav.classList.remove("is-open");
        document.body.style.overflow = "";
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    revealEls.forEach(function (el) {
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* ================================================================
     Project gallery (Our Work page + homepage featured strip)
     Reads /data/projects.json as the single source of truth.
     ================================================================ */
  var IMG_BASE = "/images/projects/";
  var STAGE_LABEL = { completed: "Completed", "in-progress": "In Progress" };

  function projectImg(coverKey, size) {
    return IMG_BASE + coverKey + "-" + size + ".jpg";
  }

  function cardHTML(p) {
    var stageClass = p.stage === "completed" ? "stage-completed" : "stage-progress";
    return (
      '<article class="project-card reveal" data-category="' + p.category + '">' +
        '<a class="thumb-wrap" href="/projects/' + p.slug + '/" aria-label="View ' + p.title + '">' +
          '<span class="stage-tag ' + stageClass + '">' + STAGE_LABEL[p.stage] + "</span>" +
          '<img src="' + projectImg(p.cover, "card") + '" alt="' + p.title + ' — ' + p.category + ', ' + p.location + '" loading="lazy" width="900" height="675">' +
        "</a>" +
        '<div class="body">' +
          '<span class="cat">' + p.category + "</span>" +
          "<h3>" + p.title + "</h3>" +
          '<p class="loc">' + p.location + "</p>" +
          '<p class="desc">' + p.short + "</p>" +
          '<a class="view-link" href="/projects/' + p.slug + '/">View project →</a>' +
        "</div>" +
      "</article>"
    );
  }

  function renderGrid(grid, projects) {
    if (!projects.length) {
      grid.innerHTML = '<p class="empty-state">No projects in this category yet — check back soon, or call Brendon to ask about a project like this.</p>';
      return;
    }
    grid.innerHTML = projects.map(cardHTML).join("");
    var newReveals = grid.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
      var io2 = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              io2.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.1 }
      );
      newReveals.forEach(function (el) {
        io2.observe(el);
      });
    } else {
      newReveals.forEach(function (el) {
        el.classList.add("is-visible");
      });
    }
  }

  function initWorkGrid() {
    var grid = document.querySelector("[data-work-grid]");
    if (!grid) return;
    var filterWrap = document.querySelector("[data-filters]");
    var featuredOnly = grid.getAttribute("data-featured-only") === "true";

    fetch("/data/projects.json")
      .then(function (r) { return r.json(); })
      .then(function (projects) {
        var list = featuredOnly ? projects.filter(function (p) { return p.featured; }) : projects;
        renderGrid(grid, list);

        if (filterWrap && !featuredOnly) {
          var categories = ["All"].concat(
            Array.from(new Set(projects.map(function (p) { return p.category; })))
          );
          filterWrap.innerHTML = categories
            .map(function (c, i) {
              return (
                '<button class="filter-btn' + (i === 0 ? " is-active" : "") + '" data-filter="' + c + '">' + c + "</button>"
              );
            })
            .join("");

          filterWrap.addEventListener("click", function (e) {
            var btn = e.target.closest(".filter-btn");
            if (!btn) return;
            filterWrap.querySelectorAll(".filter-btn").forEach(function (b) {
              b.classList.remove("is-active");
            });
            btn.classList.add("is-active");
            var cat = btn.getAttribute("data-filter");
            var filtered = cat === "All" ? projects : projects.filter(function (p) { return p.category === cat; });
            renderGrid(grid, filtered);
          });
        }
      })
      .catch(function () {
        grid.innerHTML = '<p class="empty-state">Our project gallery couldn\'t load. Please refresh, or call Brendon on <a href="tel:0225371325">022 537 1325</a>.</p>';
      });
  }
  initWorkGrid();

  /* ---------- lightbox for any <a data-lightbox> ---------- */
  var lightbox = document.querySelector(".lightbox");
  if (lightbox) {
    var lbImg = lightbox.querySelector("img");
    var lbCaption = lightbox.querySelector(".lightbox-caption");
    var lbGroup = [];
    var lbIndex = 0;

    function openLightbox(group, index) {
      lbGroup = group;
      lbIndex = index;
      updateLightbox();
      lightbox.classList.add("is-open");
      document.body.style.overflow = "hidden";
    }
    function updateLightbox() {
      var item = lbGroup[lbIndex];
      lbImg.src = item.src;
      lbImg.alt = item.alt;
      lbCaption.textContent = item.alt;
    }
    function closeLightbox() {
      lightbox.classList.remove("is-open");
      document.body.style.overflow = "";
    }
    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-lightbox]");
      if (trigger) {
        e.preventDefault();
        var groupName = trigger.getAttribute("data-lightbox");
        var nodes = Array.from(document.querySelectorAll('[data-lightbox="' + groupName + '"]'));
        var group = nodes.map(function (n) {
          return { src: n.getAttribute("href") || n.getAttribute("data-full"), alt: n.querySelector("img") ? n.querySelector("img").alt : trigger.getAttribute("data-caption") || "" };
        });
        openLightbox(group, nodes.indexOf(trigger));
      }
      if (e.target.closest(".lightbox-close") || e.target === lightbox) {
        closeLightbox();
      }
      if (e.target.closest(".lightbox-prev")) {
        lbIndex = (lbIndex - 1 + lbGroup.length) % lbGroup.length;
        updateLightbox();
      }
      if (e.target.closest(".lightbox-next")) {
        lbIndex = (lbIndex + 1) % lbGroup.length;
        updateLightbox();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (!lightbox.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") {
        lbIndex = (lbIndex - 1 + lbGroup.length) % lbGroup.length;
        updateLightbox();
      }
      if (e.key === "ArrowRight") {
        lbIndex = (lbIndex + 1) % lbGroup.length;
        updateLightbox();
      }
    });
  }

  /* ---------- quote form (Netlify Forms, AJAX submit) ---------- */
  var quoteForm = document.getElementById("quote-form");
  if (quoteForm) {
    quoteForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var data = new FormData(quoteForm);
      var submitBtn = quoteForm.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(data).toString(),
      })
        .then(function () {
          quoteForm.style.display = "none";
          var success = document.getElementById("form-success");
          if (success) success.classList.add("is-visible");
        })
        .catch(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = "Request Free Quote";
          alert("Something went wrong sending that — please call Brendon directly on 022 537 1325, or try again.");
        });
    });
  }
})();
