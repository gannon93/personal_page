THEME_COOKIE_KEY = "theme"
THEME_BASEDIR = "/static/css/gkit_css/themes/"
THEME_HEAD = "gk_theme_"

function changeTheme(theme) {
    newstylesheet = getSheetName(theme);

    if ($("#dynamic_css").length == 0) {
        $("head").append("<link>")
        css = $("head").children(":last");

        css.attr({
          id: "dynamic_css",
          rel:  "stylesheet",
          type: "text/css",
          href: newstylesheet
        });
    } else {
        $("#dynamic_css").attr("href",newstylesheet);
    }
    eraseCookie(THEME_COOKIE_KEY);
    createCookie(THEME_COOKIE_KEY, theme, 1);
}

function getSheetName(theme) {
    return (THEME_BASEDIR + THEME_HEAD + theme + ".css");
}

$(function(){
    ctheme = readCookie(THEME_COOKIE_KEY);
    if (ctheme != null && ctheme.length > 0) {
        changeTheme(ctheme);
    } else {
        changeTheme("hotline_miami");
        createCookie(THEME_COOKIE_KEY, "hotline_miami", 1)
    }
});