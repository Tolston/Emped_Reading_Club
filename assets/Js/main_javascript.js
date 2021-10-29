//custom javascript/JQuery

//actions on page load

$(window).on('load', function() {

    //open login modal on page load
        var link = document.getElementById("account_link");
        userCookie = sessionStorage.getItem('User_Name');
        if (userCookie ==  null){
            $("#login_section").modal('show');
        }
        else
        {
            document.getElementById("account_link_span").innerHTML=userCookie;
        }

    //ask permission to store location
        function getCookie(cname) {
            var name = cname + "=";
            var decodedCookie = decodeURIComponent(document.cookie);
            var ca = decodedCookie.split(';');
            for(var i = 0; i < ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0) == ' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
                }
            }
            return "";
        }

        const successCallback = (position) => {
		    console.log(position);
	    };

	    const errorCallback = (error) => {
		    console.log(position);
        };

	    navigator.geolocation.getCurrentPosition(successCallback,errorCallback);
});


//actions on document ready

$(document).ready(function(){

    // script to map login link to login form

   	    $("#login_link").click(function(){
			$("#login_section").modal();
		});

    // open sign up form and hide login form on signup form link click

		$("#signupform_link").click(function(){
	 		$("#login_div").addClass("d-none");
			$("#signup_div").removeClass("d-none");
		});

    // open login form and hide sign up form on login form link click

		$("#loginform_link").click(function(){
	 		$("#signup_div").addClass("d-none");
			$("#login_div").removeClass("d-none");
		});

    // adding country code to textbox mobile_number

//		var input = document.querySelector("#mobile_number");
//        window.intlTelInput(input, {
//            preferredCountries: ["in"],
// 	        separateDialCode: true,
// 	        initialCountry: ""
////	        geoIpLookup: function(callback) {
////	            $.get('https://ipinfo.io', function() {}, "jsonp").always(function(resp) {
////		            var countryCode = (resp && resp.country) ? resp.country : "us";
////			        callback(countryCode);
////		        });
////	        },
////	        utilsScript: "../../build/js/utils.js?1613236686837" // just for formatting/placeholders etc
//        }).on('countrychange', function (e, countryData) {
//            $("#dialcode").val(($("#mobile_number").intlTelInput("getSelectedCountryData").dialCode));
//        });
//        alert($("#mobile_number").intlTelInput("getSelectedCountryData").dialCode);
});

//window.onload = function authenticate(){
//    var name = document.getElementById("account_name").value;
//    if(name == ""){
//        document.getElementById("account_name").innerHTML = " Login";
//        $('#login_section').modal('show');
//    }
//    else{
//
//    }
//}

// open sign up form
function signup_form(){
    document.getElementById("signup_div").classList.remove("d-none");
    document.getElementById("login_div").classList.add("d-none");
}

// open login form
function login_form(){
    document.getElementById("login_div").classList.remove("d-none");
    document.getElementById("signup_div").classList.add("d-none");
}

// validating phone number and requesting to send otp
function send_otp(){
    var number = document.getElementById("mobile_number");
    var validation_msg=document.getElementById("validation_msg");
    var regex = /^\d{10}$/;
    if(!number.value.match(regex)){
        validation_msg.classList.remove("d-none");
        number.classList.add("textbox-error");
    }
    else{
        validation_msg.classList.add("d-none");
        number.classList.remove("textbox-error");
    }
}

// validating all inputs and signing up

function validate_signup(){
    var fname = document.getElementById("input_fname");
    var lname = document.getElementById("input_lname");
    var door = document.getElementById("input_doorno");
    var address = document.getElementById("input_address");
    var landmark = document.getElementById("input_landmark");
    if(fname.value==""){
        fname.classList.add("textbox-error");
    }
    else{
        fname.classList.remove("textbox-error");
    }
    if(door.value==""){
        door.classList.add("textbox-error");
    }
    else{
        door.classList.remove("textbox-error");
    }
    if(address.value==""){
        address.classList.add("textbox-error");
    }
    else{
        address.classList.remove("textbox-error");
    }
    if(landmark.value==""){
        landmark.classList.add("textbox-error");
    }
    else{
        landmark.classList.remove("textbox-error");
    }
}



// to open sidebar
function open_sidebar(){
    var w = document.documentElement.clientWidth;
    if (w < 400){
        document.getElementById("menu_sidebar").style.width="35%";
    }
    else{
        document.getElementById("menu_sidebar").style.width="25%";
    }
}

// to close sidebar
function closeNav(){
    document.getElementById("menu_sidebar").style.width="0%";
}

//to display current reading on main space if screen is large
function btn_current_reading(){
    var w = document.documentElement.clientWidth;
    var target_section = document.getElementById("div_profile_invite_display");
    var current_section = document.getElementById("div_current_reading");
    var a_current_link = document.getElementById("current_reading_link");
    if(w>575){
        a_current_link.setAttribute("data-target","#div_profile_invite_display");
        a_current_link.setAttribute("aria-controls","div_profile_invite_display");
        a_current_link.removeAttribute("data-toggle");
        target_section.setAttribute("aria-labelledby","header_current_reading");
        target_section.setAttribute("data-bs-parent","div_accordion_profile");
        target_section.innerHTML=current_section.innerHTML;
    }
    else{
        a_current_link.setAttribute("data-toggle","collapse");
        a_current_link.setAttribute("data-target","#div_current_reading");
        a_current_link.setAttribute("aria-controls","div_current_reading");
    }
}

//to display return book on main space if screen is large
function btn_return_book(){
    var w = document.documentElement.clientWidth;
    var target_section = document.getElementById("div_profile_invite_display");
    var current_section = document.getElementById("div_return_book");
    var a_current_link = document.getElementById("return_book_link");
    if(w>575){
        a_current_link.setAttribute("data-target","#div_profile_invite_display");
        a_current_link.setAttribute("aria-controls","div_profile_invite_display");
        a_current_link.removeAttribute("data-toggle");
        target_section.setAttribute("aria-labelledby","header_return_book");
        target_section.setAttribute("data-bs-parent","div_accordion_profile");
        target_section.innerHTML=current_section.innerHTML;
    }
    else{
        a_current_link.setAttribute("data-toggle","collapse");
        a_current_link.setAttribute("data-target","#div_return_book");
        a_current_link.setAttribute("aria-controls","div_return_book");
    }
}



//to display history wallet on main space if screen is large
function btn_history_wallet(){
    var w = document.documentElement.clientWidth;
    var target_section = document.getElementById("div_profile_invite_display");
    var current_section = document.getElementById("div_history_wallet");
    var a_current_link = document.getElementById("history_wallet_link");
    if(w>575){
        a_current_link.setAttribute("data-target","#div_profile_invite_display");
        a_current_link.setAttribute("aria-controls","div_profile_invite_display");
        a_current_link.removeAttribute("data-toggle");
        target_section.setAttribute("aria-labelledby","header_history_wallet");
        target_section.setAttribute("data-bs-parent","div_accordion_profile");
        target_section.innerHTML=current_section.innerHTML;
    }
    else{
        a_current_link.setAttribute("data-toggle","collapse");
        a_current_link.setAttribute("data-target","#div_history_wallet");
        a_current_link.setAttribute("aria-controls","div_history_wallet");
    }
}

//to display invite friends on main space if screen is large
function btn_invite_friends(){
    var w = document.documentElement.clientWidth;
    var target_section = document.getElementById("div_profile_invite_display");
    var current_section = document.getElementById("div_invite_friends");
    var a_current_link = document.getElementById("invite_friends_link");
    if(w>575){
        a_current_link.setAttribute("data-target","#div_profile_invite_display");
        a_current_link.setAttribute("aria-controls","div_profile_invite_display");
        a_current_link.removeAttribute("data-toggle");
        target_section.setAttribute("aria-labelledby","header_invite_friends");
        target_section.setAttribute("data-bs-parent","div_accordion_invite");
        target_section.innerHTML=current_section.innerHTML;
    }
    else{
        a_current_link.setAttribute("data-toggle","collapse");
        a_current_link.setAttribute("data-target","#div_invite_friends");
        a_current_link.setAttribute("aria-controls","div_invite_friends");
    }
}

//to display join club on main space if screen is large
function btn_join_club(){
    var w = document.documentElement.clientWidth;
    var target_section = document.getElementById("div_profile_invite_display");
    var current_section = document.getElementById("div_join_club");
    var a_current_link = document.getElementById("join_club_link");
    if(w>575){
        a_current_link.setAttribute("data-target","#div_profile_invite_display");
        a_current_link.setAttribute("aria-controls","div_profile_invite_display");
        a_current_link.removeAttribute("data-toggle");
        target_section.setAttribute("aria-labelledby","header_join_club");
        target_section.setAttribute("data-bs-parent","div_accordion_invite");
        target_section.innerHTML=current_section.innerHTML;
    }
    else{
        a_current_link.setAttribute("data-toggle","collapse");
        a_current_link.setAttribute("data-target","#div_join_club");
        a_current_link.setAttribute("aria-controls","div_join_club");
    }
}

// to scroll left for book grid
function btn_grid_scroll_left(div_id){
    var div_element = document.getElementById(div_id);
    div_element.scrollLeft -= 1000;
}


// to scroll right for book grid
function btn_grid_scroll_right(div_id){
    div_element = document.getElementById(div_id);
    div_element.scrollLeft += 1000;
}