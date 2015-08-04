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
  
  $( ".menu-icon" ).click(function() {
    $( ".site-nav .trigger" ).toggle();
  });
});
