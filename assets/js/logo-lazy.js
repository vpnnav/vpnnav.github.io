(function () {
  var imgs = document.querySelectorAll("img.js-logo[data-logo]");
  if (!imgs.length) return;

  var queue = [];
  var active = 0;
  var maxActive = 3;

  function pump() {
    while (active < maxActive && queue.length) {
      load(queue.shift());
    }
  }

  function load(img) {
    if (!img || img.getAttribute("data-logo-state")) return;
    var url = img.getAttribute("data-logo");
    if (!url) return;
    img.setAttribute("data-logo-state", "loading");
    active += 1;
    var pre = new Image();
    try {
      pre.fetchPriority = "low";
    } catch (e) {}
    pre.onload = function () {
      img.src = url;
      img.setAttribute("data-logo-state", "done");
      active -= 1;
      pump();
    };
    pre.onerror = function () {
      img.setAttribute("data-logo-state", "done");
      active -= 1;
      pump();
    };
    pre.src = url;
  }

  function enqueueAll() {
    Array.prototype.forEach.call(imgs, function (img) {
      queue.push(img);
    });
    pump();
  }

  if (!("IntersectionObserver" in window)) {
    enqueueAll();
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      queue.push(entry.target);
      pump();
    });
  }, { rootMargin: "160px 0px" });

  Array.prototype.forEach.call(imgs, function (img) {
    observer.observe(img);
  });
})();
