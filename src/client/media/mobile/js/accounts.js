// accounts.js
// Handles authentication, registration, login
// Dependencies: jQuery

var accounts = (function($, d3, console) {
    // Enable strict javascript interpretation
    "use strict";
    // a function to pull up the registration prompt

    function showRegister() {
        $('.register').slideDown();
        $('#finishRegistration').click(function() {});
    }

    function showCommentInput() {
        $('.comment-input').slideDown();
    }

    // a function to pull up the login prompt.

    function showLogin() {
        $('.landing').slideUp();
        $('.login').slideDown();
    }

    //function that determines if the user has already rated 2 comments
    // and should now login/ register to move forward.

    function readyToLogin() {
        return window.ratings && window.ratings.length >= 2;
    }

    // function that determines if the user should register to continue
    // it returns true when both the registration sliders have been saved.

    function mustRegister() {
        return window.sliders && window.sliders.length >= 1;
    }

    //function that removes the landing page and populates the map when the first time button is clicked.

    function firstTime() {
        utils.showLoading("Loading the garden...", function() {
            utils.ajaxTempOff(blooms.populateBlooms);

            setTimeout(function() { // d3 needs a little extra time to load
                $('.landing').slideUp('fast', function() {
                    utils.hideLoading(1000);
                });
            }, 1500);
        });
    }
    // Checks to see if the user has logged in and sets window.authentiated.
    // This is used to change the behavior of the site for users
    // that have logged in. (Mostly to send data to server immediately)

    function setAuthenticated() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                window.authenticated = data['is_user_authenticated'];
            });
        });

        return window.authenticated;
    }

    //@logindata - data is in a serialized form
    //This function is used specifically to login right after registration. This function also
    //  sends the data that has been stored in the window to the server after a successful the login.

    function loginAfterRegister(loginData) {
        $.ajax({
            url: window.url_root + '/accountsjson/login/',
            type: 'POST',
            dataType: 'json',
            data: loginData,
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    console.log("successful login detected!!");
                    rate.sendComment(window.comment);

                    for (var i = 1; i <= window.num_sliders; i++) {
                        rate.sendSlider(window.sliders['s' + i], i);
                    }

                    for (i = 0; i < window.ratings.length - 1; i++) {
                        rate.sendAgreementRating(window.ratings[i]);
                        rate.sendInsightRating(window.ratings[i]);
                    }

                    rate.sendAgreementRating(window.ratings[window.ratings.length - 1]);
                    rate.sendInsightRating(window.ratings[window.ratings.length - 1]);
                    //window.authenticated = true;
                } else {
                    // we should rerender the form here.
                }
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });
    }


    function loadMyCommentDiv() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                try {
                    var comment = data['cur_user_comment'][0][0];
                    $('.comment-text').html(comment);
                    $('.edit-comment-box').html(comment);
                } catch (err) {
                    // probably an admin user or something. they didn't have a comment
                }
            });
        });

        $('.my-comment').slideDown();
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

    }

    /** Sets the field ".num-rated-by" to the number of people who've rated the 
     *  users comment. */
    function setNumRatedBy() {
        utils.ajaxTempOff(function() {
            $.getJSON(window.url_root + '/os/ratedby/1/', function(data) {
                $('.num-rated-by').text(data['sorted_comments_ids'].length);
            });

        });
    }

    /** Sets up all the stuff that loggedIn users expect and need. 
     *  JUSTREGISTERED is a boolean and optional. Used to shortcircuit showGraphs.
     */
    function initLoggedInFeatures(justRegistered) {
        justRegistered = typeof justRegistered !== 'undefined' ? justRegistered : false;

        rate.initMenubar();

        utils.ajaxTempOff(function() {
            stats.showGraphs(justRegistered);

            //var data = $.getJSON(window.url_root + '/os/show/1/');
            $.getJSON(window.url_root + '/os/show/1/', function(data) {
                $('.score-value').text(data['cur_user_rater_score']);
                window.user_score = data['cur_user_rater_score'];
                $('.username').text(' ' + data['cur_username']);
            });

        });

        setNumRatedBy();
    }

    return {
        'showCommentInput': showCommentInput,
        'showRegister': showRegister,
        'showLogin': showLogin,
        'readyToLogin': readyToLogin,
        'mustRegister': mustRegister,
        'firstTime': firstTime,
        'setAuthenticated': setAuthenticated,
        'loginAfterRegister': loginAfterRegister,
        'loadMyCommentDiv': loadMyCommentDiv,
        'initLoggedInFeatures': initLoggedInFeatures
    };

})($, d3, console);

$(document).ready(function() {
    $('#reg_form').submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        //The following set of code is needed to format the data for the login which occurs after the registration
        var serializedData = $(this).serializeArray();
        var names = serializedData.map(function(r) {
            return r.name;
        });
        var index_user = names.indexOf("regusername");
        var index_pass = names.indexOf("regpassword1");
        //var index_email = names.indexOf("regemail");

        var data2 = {};
        data2["username"] = serializedData[index_user].value;
        data2["password1"] = serializedData[index_pass].value;
        data2["password"] = serializedData[index_pass].value;
        data2["password2"] = serializedData[index_pass].value;
        //data2["email"] = serializedData[index_email].value;

        var serializedFormData = $(this).serialize();

        utils.ajaxTempOff(function() {
            $.ajax({
                url: window.url_root + '/accountsjson/register/',
                type: 'POST',
                dataType: 'json',
                data: data2,
                success: function(data) {
                    $("#username-error").hide();
                    //$("#email-error").hide();
                    $("#password-error").hide();

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Creating your bloom...", function() {
                                accounts.loginAfterRegister(data2);
                                blooms.populateBlooms();
                                accounts.initLoggedInFeatures(true);

                            setTimeout(function() { //give d3 some extra time
                                $('.register').slideUp('fast', function() {
                                    utils.hideLoading(1000);
                                });
                                }, 1500);

                            
                        });
                        //accounts.setAuthenticated();
                    } else {
                        accounts.showRegister();
                        if (data.hasOwnProperty('form_errors')) {

                            var errors = data['form_errors'];

                            if ('username' in errors) {
                                $("#username-error").html(errors['username']);
                                $("#username-error").show();
                            }

                           /* if ('email' in errors) {
                                $("#email-error").html(errors['email']);
                                $("#email-error").show();
                            }*/

                            if ('password1' in errors) {
                                $("#password-error").html(errors['password1']);
                                $("#password-error").show();
                            }

                            $('#register').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
                        }
                    }
                },
                error: function() {
                    console.log("ERROR posting registration request. Abort!");
                },
            });
        });
    });

    $('#login_form').submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var serializedFormData = $(this).serialize();

        utils.ajaxTempOff(function() {
            $.ajax({
                url: window.url_root + '/accountsjson/login/',
                type: 'POST',
                dataType: 'json',
                data: serializedFormData,
                success: function(data) {
                    $("#login-error").hide();

                    if (data.hasOwnProperty('success')) {
                        accounts.setAuthenticated();
                        utils.showLoading("Loading...", function() {
                            blooms.populateBlooms();
                            accounts.initLoggedInFeatures();

                            setTimeout(function() { // d3 needs a little extra time to load
                                $('.login').slideUp('fast', function() {
                                    utils.hideLoading(1000);
                                });
                            }, 1000);
                        });
                    } else {
                        console.log("Failed login attempt");
                        $('#login-error').text(data['form_errors'].__all__[0]);
                        $("#login-error").show();
                        $('#login').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

                    }
                },
                error: function() {
                    console.log("ERROR posting login request. Abort!");
                }
            });
        });

    });

    $('.first-time-btn').click(function() {
        accounts.firstTime();
    });

    $('.login-btn').click(function() {
        accounts.showLogin();
    });

    $('.my-comment-btn').click(function() {
        accounts.loadMyCommentDiv();
    });

    $('.edit-comment-btn').click(function() {
        $('.comment-region').hide();
        $('.edit-comment').show();
    });

    $('.edit-comment-save-btn').click(function() {
        rate.sendComment($('.edit-comment-box').val());
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');

        $('.my-comment').slideUp('slow', function() {
            $('.edit-comment').hide();
            $('.comment-region').show();
        });
    });

    $('.edit-comment-cancel-btn').click(function() {
        $('.comment-region').show();
        $('.edit-comment').hide();
    });

    $('.edit-comment-done-btn').click(function() {
        $('.menubar').find('.ui-btn-active').removeClass('ui-btn-active ui-focus');
        $('.my-comment').slideUp();
    });

    $('.logout-btn').click(function(e) {
        $('.logout').show();
        e.preventDefault();
        e.stopPropagation();

        $.ajax({
            url: window.url_root + '/accountsjson/logout/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                if (data.hasOwnProperty('success')) {
                    // TODO: this needs to be cleaned up into some sort of function
                    // and this logic is shitty and it's not resetting the score labels well
                    //$('.landing').show();
                    window.user_score = undefined;
                    window.authenticated = false;
                    $('.menubar').hide();
                    $('#instructions').show();
                    $('.inst-score').hide();
                    rate.resetEndSliders();
                } else {}
            },
            error: function() {
                console.log("ERROR posting login request. Abort!");
            }
        });

    });

    $('.logout-start-over').click(function() {
        $('.landing').slideDown();
        $('.logout').slideUp();
    });

    $('.logout-login-again').click(function() {
        $('.logout').slideUp();
        $('.login').slideDown();
    });

});