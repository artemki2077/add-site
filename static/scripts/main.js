const header = document.querySelector('.header')
const body = document.querySelector('body');
const Links = document.querySelectorAll('.link');


$("body").on('click', '[href*="#"]', function(e){
    var fixed_offset = 100;
    $('html,body').stop().animate({ scrollTop: $(this.hash).offset().top - fixed_offset }, {
        duration: 600, // тут можно контролировать скорость
        easing: "swing"
     });
    e.preventDefault();
  });