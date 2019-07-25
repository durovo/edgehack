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

function stop_excercise(ele, conv) {
    $.getJSON('/stop',
        function(data) {
            console.log("Stopping Excercise");
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
    var stop_button = $('#stop-excercise')
    stop_button.bind('click', function() {
        stop_excercise();
        return false;
    });

    var squats_button =  $('#start-squats')
    squats_button.bind('click', function() {
        start_squats();
        return false;
    });

    var bicepcurls_button =  $('#start-bicepcurls')
    bicepcurls_button.bind('click', function() {
        start_bicepcurls();
        return false;
    });

    var pushups_button =  $('#start-pushups')
    pushups_button.bind('click', function() {
        start_pushups();
        return false;
    });
});