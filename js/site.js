(function () {
  var button = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (button && nav) {
    button.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      button.setAttribute("aria-expanded", open ? "true" : "false");
      button.textContent = open ? "Close" : "Menu";
    });
  }

  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (event) {
      if (!form.getAttribute("action")) {
        event.preventDefault();
        var status = document.getElementById("form-status");
        if (status) {
          status.textContent = "This form is not connected yet. Please call Joe Moraca at 386-288-9689.";
        }
      }
    });
  }

  var search = document.getElementById("site-search");
  if (search && Array.isArray(window.SITE_PAGES)) {
    var results = document.getElementById("search-results");
    search.addEventListener("submit", function (event) {
      event.preventDefault();
      var input = search.querySelector("input");
      var query = (input && input.value ? input.value : "").trim().toLowerCase();
      if (!results) {
        return;
      }
      results.innerHTML = "";
      if (!query) {
        return;
      }
      var found = window.SITE_PAGES.filter(function (page) {
        return (page.title + " " + page.text).toLowerCase().indexOf(query) !== -1;
      });
      if (!found.length) {
        var empty = document.createElement("li");
        empty.textContent = "No matching pages.";
        results.appendChild(empty);
        return;
      }
      found.forEach(function (page) {
        var item = document.createElement("li");
        var link = document.createElement("a");
        link.href = page.url;
        link.textContent = page.title;
        item.appendChild(link);
        results.appendChild(item);
      });
    });
  }
})();
