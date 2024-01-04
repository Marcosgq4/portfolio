$(document).ready(function() {

    $('.navbar-toggle').click(function() {
        $(this).toggleClass('act');
            if($(this).hasClass('act')) {
                $('.main-menu').addClass('act');
            }
            else {
                $('.main-menu').removeClass('act');
            }
    });

    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $(document).on('click', '.page-scroll a', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1000, 'easeInOutExpo');
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.site-header',
        offset: 10
    });

	/* Progress bar */
    var $section = $('.section-skills');
    function loadDaBars() {
	    $('.progress .progress-bar').progressbar({
	        transition_delay: 500
	    });
    }
    
    $(document).bind('scroll', function(ev) {
        var scrollOffset = $(document).scrollTop();
        var containerOffset = $section.offset().top - window.innerHeight;
        if (scrollOffset > containerOffset) {
            loadDaBars();scrolsl
            // unbind event not to load  again
            $(document).unbind('scroll');
        }
    });

    /* Counters  */
    if ($(".section-counters .start").length>0) {
        $(".section-counters .start").each(function() {
            var stat_item = $(this),
            offset = stat_item.offset().top;
            $(window).scroll(function() {
                if($(window).scrollTop() > (offset - 1000) && !(stat_item.hasClass('counting'))) {
                    stat_item.addClass('counting');
                    stat_item.countTo();
                }
            });
        });
    };

	// another custom callback for counting to infinity
	$('#infinity').data('countToOptions', {
		onComplete: function (value) {
		  count.call(this, {
		    from: value,
		    to: value + 1
		  });
		}
	});

	$('#infinity').each(count);

	function count(options) {
        var $this = $(this);
        options = $.extend({}, options || {}, $this.data('countToOptions') || {});
        $this.countTo(options);
    }

    // Navigation overlay
    var s = skrollr.init({
            forceHeight: false,
            smoothScrolling: false,
            mobileDeceleration: 0.004,
            mobileCheck: function() {
                //hack - forces mobile version to be off
                return false;
            }
    });
    
    $('.auth-check').click(function(event) {
        var projectUrl = $(this).data('project-url');
        checkAuthAndRedirect(event, projectUrl);
    });

    // checkAuthAndRedirect function and other existing functions
    window.checkAuthAndRedirect = function(event, projectUrl) {
        event.preventDefault();
        console.log('Function called');

        if (window.isUserAuthenticated) {
            window.location.href = projectUrl; // Redirect to project
        } else {
            // Show popup for non-authenticated users
            var loginUrl = window.loginUrl + '?next=' + encodeURIComponent(projectUrl);
            showAuthPopup(loginUrl, projectUrl);
        }
    };

    function showAuthPopup(loginUrl, projectUrl) {
        $('#loginButton').attr('href', loginUrl + '?next=' + encodeURIComponent(projectUrl));
        
        $('#guestButton').off('click').on('click', function(event) {
            event.preventDefault();
            handleGuestAccess(projectUrl); // Call the new function for guest access
        });

        $('#authModal').modal('show');
    }

    // Attach the event listener for all links that require authentication check
    $('a[data-auth-required="true"]').on('click', function(event) {
        var projectUrl = $(this).attr('href'); // The URL to redirect to
        checkAuthAndRedirect(event, projectUrl);
    });

    function handleGuestAccess(projectUrl) {
        $.ajax({
            url: '/continue-as-guest/', // URL to your guest login view
            type: 'POST',
            data: { 'project_url': projectUrl },
            headers: { 'X-CSRFToken': getCsrfToken() },

            success: function(response) {
                window.location.href = response.redirect_url; // Redirect to the project URL
            },
            
            error: function(xhr, status, error) {
                console.error('Error logging in as guest. Status:', status, 'Error:', error);
            }
        });
    }

    function getCsrfToken() {
        var name = 'csrftoken';
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});

window.isUserAuthenticated = false;