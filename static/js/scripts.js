const url_base= "http://127.0.0.1:8000"

//Check if user exist with this password
function login(url, token) {
    url = url_base+url;
    var user = $("#user").val();
    var password = $("#password").val();
    $("#user").val("");
    $("#password").val("");
    if (user === "" || password === ""){
        toastr.options = {
              "closeButton": false,
              "debug": false,
              "newestOnTop": false,
              "progressBar": false,
              "positionClass": "toast-bottom-center",
              "preventDuplicates": false,
              "onclick": null,
              "showDuration": "300",
              "hideDuration": "1000",
              "timeOut": "5000",
              "extendedTimeOut": "1000",
              "showEasing": "swing",
              "hideEasing": "linear",
              "showMethod": "fadeIn",
              "hideMethod": "fadeOut"
            }
            toastr.error("Usuario o contraseña vacio");
    }
    else {
        var data = '{ "user": "'+ user +'", "password": "'+ password +'"}';
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: url,
            type: 'POST',
            data: data,
            success:function(response) {
                var json = JSON.parse(response);
                var url = json['url'];
                window.location.href = url;
            },
            error:function (response) {
                toastr.options = {
                  "closeButton": false,
                  "debug": false,
                  "newestOnTop": false,
                  "progressBar": false,
                  "positionClass": "toast-bottom-center",
                  "preventDuplicates": false,
                  "onclick": null,
                  "showDuration": "300",
                  "hideDuration": "1000",
                  "timeOut": "5000",
                  "extendedTimeOut": "1000",
                  "showEasing": "swing",
                  "hideEasing": "linear",
                  "showMethod": "fadeIn",
                  "hideMethod": "fadeOut"
                }
                toastr.error("Usuario o contraseña incorrecto");
            }
        });
    }

};

function do_logout(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
            var url = json['url'];
            window.location.href = url;
        }
    });
}

function school_calendar(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
            var html = json['html'];
            $("#main_base").html(html);
        }
    });
}

//dropdown, show subjects and change image 
function dropdown(up, down) {
    //Miramos si existe id = hidden si no es que hay que cerrarlo y cambiar la imagen
    var asignaturas_hidden = $(".hidden");
    var asignaturas_visible = $('.visible');
    var mySubjects = $(".my_subjects");
    if (asignaturas_hidden.length === 0 && 0 !== asignaturas_visible.length) {
        mySubjects.text("My Subjects ▼");
        for (i = 0; i< asignaturas_visible.length; i++){
            $(asignaturas_visible[i]).css("display", "none");
            $(asignaturas_visible[i]).attr("class", "hidden practica_name");
        }
    }
    else if (asignaturas_visible.length === 0 && 0 !== asignaturas_hidden.length){
        mySubjects.text("My Subjects ▲");
        for (i = 0; i< asignaturas_hidden.length; i++){
            $(asignaturas_hidden[i]).show();
            $(asignaturas_hidden[i]).attr("class", "visible practica_name");
        }
    }
}

function asignatura(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
            var url = json['url'];
            window.location.href = url;
        }
    });
}

function go_create_practica(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
            var url = json['url'];
            window.location.href = url;
        }
    });
}

function go_practica(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
             var url = json['url'];
            window.location.href = url;
        }
    });
}

function show_enunciado(url) {
    url = url_base+url;
    window.location.href = url;
}

function show_guia_docente(url) {
    url = url_base+url;
    window.location.href = url;
}

function show_pdf_grupos(url) {
    url = url_base+url;window.location.href = url;window.location.replace(url);
}

function alumnos_grupos_text(url, token) {
    url = url_base+url;
    $.ajax({
        headers: { "X-CSRFToken": token },
        url: url,
        success:function(response) {
            var json = JSON.parse(response);
             var url = json['url'];
            window.location.href = url;
        }
    });
}