$("#alert_validate").hide()

function check_in() {

    $.ajax({
        url: "/workings",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json"
        , success: () => {
            console.log("CAll API OK")
        }
    }).done(function (res) {
        console.log(res)
        document.getElementById("alert_validate").innerHTML = "Check_in successfully";
        $("#alert_validate").show();
        $("#alert_validate").hide(7000);

    });
}

function cal_absen_days() {

    rest_allowed_day = document.getElementById("rest_allowed_day").value;
    // console.log(1,rest_allowed_day)
    var time_from = document.getElementById("time_from").value;
    var time_to = document.getElementById("time_to").value;


    var hour_from = document.getElementById("hour_from").value;
    var hour_to = document.getElementById("hour_to").value;
    time_to = time_to + " " + hour_to + ":00";
    time_from = time_from + " " + hour_from + ":00";
    var sum_absen_days_origin = new Date(time_to).getTime() - new Date(time_from).getTime();

    if (sum_absen_days_origin < 0) {
        document.getElementById("alert_validate").innerHTML = "Thông tin ngày không chính xác";
        $("#alert_validate").show();
        $("#alert_validate").hide(7000);
        $("#time-to").focus();
        return false;
    }

    sum_absen_days = sum_absen_days_origin / (1000 * 3600 * 24);
    sum_absen_hour = Math.round((sum_absen_days - Math.floor(sum_absen_days)) * 24);

    // console.log(sum_absen_hour);
    if (sum_absen_hour <= 4 && sum_absen_hour >= 1)
        sum_absen_days = Math.floor(sum_absen_days) + 0.5;
    else if (sum_absen_hour > 4)
        sum_absen_days = Math.floor(sum_absen_days) + 1;
    else
        sum_absen_days = Math.floor(sum_absen_days);
    // console.log(sum_absen_days_origin)

    if (sum_absen_days > rest_allowed_day) {
        console.log(sum_absen_days, rest_allowed_day)
        document.getElementById("alert_validate").innerHTML = "Vượt quá số ngày cho phép";
        $("#alert_validate").show(1000);
        $("#alert_validate").hide(7000);


        return;
    }
    if (sum_absen_days <= 0) {
        // console.log(sum_absen_days ,rest_allowed_day )
        document.getElementById("alert_validate").innerHTML = "Số ngày nghỉ ko hợp lệ";
        $("#alert_validate").show();
        $("#alert_validate").hide(7000);

        return;
    }

    // console.log(sum_absen_days)

    $("#sum_absen_days").val(sum_absen_days);

    return 1;

}

function post_absence() {
    if (!cal_absen_days()) {
        return
    }
    // console.log("123");
    var reason = document.getElementById("reason").value;
    var time_from = document.getElementById("time_from").value;
    var time_to = document.getElementById("time_to").value;

    var hour_from = document.getElementById("hour_from").value;
    var hour_to = document.getElementById("hour_to").value;

    var flag_allow = $('#flag_allow').find(":selected").val();

    // console.log(new Ti-hour_from);
    time_to = time_to + " " + hour_to + ":00";
    time_from = time_from + " " + hour_from + ":00";

    data = {"reason": reason, "time_from": time_from, "time_to": time_to,"flag_allow":flag_allow};
    url = "/absences";
    console.log(data)
    $.ajax({
        data: JSON.stringify(data),
        url: url,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json"
        , success: (res) => {
            console.log(res)
        }
    }).done(function (res) {
        document.getElementById("alert_validate").innerHTML = "Đăng kí nghỉ thành công";
        $("#alert_validate").show();
        $("#alert_validate").hide(7000);

        // window.location.reload();


    });
}
function post_add_wk() {

    var reason = document.getElementById("reason_add_wk").value;
    var time_from = document.getElementById("time_from_add_wk").value;
    var time_to = document.getElementById("time_to_add_wk").value;

    var hour_from = document.getElementById("hour_from_add_wk").value;
    var hour_to = document.getElementById("hour_to_add_wk").value;


    // console.log(new Ti-hour_from);
    time_to = time_to + " " + hour_to + ":00";
    time_from = time_from + " " + hour_from + ":00";

    data = {"reason": reason, "time_from": time_from, "time_to": time_to};
    url = "/add_wks";
    console.log(data)
    $.ajax({
        data: JSON.stringify(data),
        url: url,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        dataType: "json"
        , success: (res) => {
            console.log(res)
        }
    }).done(function (res) {
        document.getElementById("alert_validate_add_wk").innerHTML = "Đăng kí bổ sung thành công";
        $("#alert_validate_add_wk").show();
        $("#alert_validate_add_wk").hide(7000);

        // window.location.reload();


    });
}
 function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length);
    }
  }
  return "";
}
  function login(){

    email = document.getElementById("email").value
    pass_word = document.getElementById("pass_word").value
    console.log(email,pass_word)
    user = {"email": email,"pass_word": pass_word}
    // var obj = jQuery.parseJSON( user );
    console.log(user.type)
    $.ajax({url:"/token",
    type:"POST",
    contentType:"application/json; charset=utf-8",
    dataType:"json",
      data:  JSON.stringify(user)
      ,success : () => {
        console.log("CAll API OK")
      }
      }).done(function(res) {
        document.cookie = "access_token" + " = " +  res.access_token
      window.location.replace("http://127.0.0.1:8081/check_in");

});


            }

  $("#login").click(function (e){
    e.preventDefault();
    console.log("LOGIN")
    login();
          });



$("#submit_absence").click(function (e) {
    e.preventDefault();
    post_absence();
});
$("#submit_add_wk").click(function (e) {
    e.preventDefault();
    post_add_wk();
});
$("#time_from").blur(function (e) {
    e.preventDefault();
    cal_absen_days();
});
$("#time_to").blur(function (e) {
    e.preventDefault();
    cal_absen_days();
});
$("#sum_absen_days").click(function (e) {
        e.preventDefault();
        cal_absen_days();
    }
);


$("#check_in").click(function (e) {
        e.preventDefault();
        check_in();
    });
$("#user-profile").click(function (e) {
e.preventDefault();
// alert(123)
});
$("#logout").click(function (e) {
e.preventDefault();
// alert(123)
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.
    location.reload();
});



