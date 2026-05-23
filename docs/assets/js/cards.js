document.addEventListener("page:loaded", function() {
    ["apps", "projects"].forEach(function(uid) {
      var fn = window["filterCards_" + uid];
      if (typeof fn === "function") fn("");
    });
  });