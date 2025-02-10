$(".nav>li").each(function() {
    var navItem = $(this);
    navItem
    if (navItem.find("a").attr("href") === location.pathname) {
      navItem.find("a").addClass("active");
    } else {
        navItem.find("a").removeClass("active");
    }
});