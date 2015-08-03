$(document).ready(function(){
  jQuery('li a').each(function() {
    if (jQuery(this).attr('href')  ===  window.location.pathname) {
      jQuery(this).addClass('active');
    }
  });

  $(".post h2").each(function(){
    $(".side li a.active ~ nav").append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a href='#" +           $(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,'') + "'>" + $(this).text() + "</a></li>");
    $(this).attr("id",$(this).text().toLowerCase().replace(/ /g, '-').replace(/[^\w-]+/g,''));
  });

  var $elSiteNav = $('.site-nav');
  $elSiteNav.on('touchstart', function(e) {
  	$('.trigger').addClass('expanded');
  });
  $elSiteNav.on('mouseenter mouseleave', function(e) {
  	$('.trigger').toggleClass('expanded');
  });
  $('body').on('click touchstart', function(e) {
  	if (!$elSiteNav.is(e.target) && $elSiteNav.has(e.target).length === 0) {
        $('.trigger').removeClass('expanded');
    }
  });

});
