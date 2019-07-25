// $(document).ready(function(){
//     var socket = io.connect('http://' + document.domain + ':' + location.port);
//     socket.on('connect', function() {
//         socket.emit('uisend', {data: 'I am UI calling to python!'});
//     });
//     socket.on("pysend", function(msg) {
//         console.log("yes baby 2:"+msg.data)
//      });
// });

// function botintro(ele,conv) {
//     $.getJSON('/botintro',
//             function(data) {
//                 console.log(data)
//                 ele.html(data.buttonName)
//                 var convtag = '<p class="convtag">'+ data.botanswers +'</p>'
//                 conv.append(convtag)
//         });
// }
// function humanIntro(ele,conv) {
//     $.getJSON('/humanIntro',
//             function(data) {
//                 console.log(data)
//                 ele.html(data.buttonName)
//                 var convtag = '<p class="convtag">'+ data.botanswers +'</p>'
//                 conv.append(convtag)
//         });
// }
// function askExercise(ele,conv) {
//     $.getJSON('/askExercise',
//             function(data) {
//                 console.log(data)
//                 ele.html(data.buttonName)
//                 var convtag = '<p class="convtag">'+ data.botanswers +'</p>'
//                 conv.append(convtag)
//         });
// }

function start_bicepcurls(ele,conv) {
    $.getJSON('/bicepcurls',
            function(data) {
                console.log("starting bicepcurls...")
        });
}

function start_pushups(ele,conv) {
    $.getJSON('/pushups',
            function(data) {
                console.log("starting pushups...")
        });
}

function start_squats(ele,conv) {
    $.getJSON('/squats',
            function(data) {
                console.log("starting squats...")
        });
}



function stop_exercise(ele, conv) {
    $.getJSON('/stop',
        function(data) {
            console.log("Stopping Excercise");
            $('#name').val("");
        }
    );
}

$(function() {
    var conv = $("#conversations");
    // var ele =  $('#circle-object')
    // ele.bind('click', function() {
    //     botintro(ele,conv);
    //     setTimeout(() => {
    //         humanIntro(ele,conv);
    //     }, 5000);
    //     setTimeout(()=>{
    //         askExercise(ele,conv);
    //     },11000)
    //     return false;
    // });
    function start_exercise(exercise) {
        var name_box = $('#name');

        if (name_box.val().length == 0)
        {
            name_box.addClass('important');
            return false;
        }

        flip_buttons(false);
        exercise(name_box.val());
        return false;
    }

    var name_box = $('#name');
    name_box.on('keydown', function(){
        name_box.removeClass('important');
    });

    var stop_button = $('#stop-exercise')
    stop_button.bind('click', function() {
        flip_buttons(true);
        stop_exercise();
        return false;
    });

    var squats_button =  $('#start-squats')
    squats_button.bind('click', function() {
        return start_exercise(start_squats);
    });

    var bicepcurls_button =  $('#start-bicepcurls')
    bicepcurls_button.bind('click', function() {
        return start_exercise(start_bicepcurls);
    });

    var pushups_button =  $('#start-pushups')
    pushups_button.bind('click', function() {
        return start_exercise(start_pushups);
    });

    exercise_buttons = [squats_button, bicepcurls_button, pushups_button]
    function flip_buttons(display)
    {
        exercise_buttons.forEach(element => {
            console.log(element)
            if (display)
            {
                element.show();
            }
            else 
            {
                element.hide();
            }
        });
        if (display)
        {
            stop_button.hide();
        }
        else 
        {
            stop_button.show();
        }
    }
});