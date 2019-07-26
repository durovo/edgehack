
function updateLeaderBoard(data, exercise)
{
    var boardData = data[exercise];
    var board = $('#'+exercise+'_board');
    count = 1;
    board.empty();
    board.append(`<div class="leaderboard-header flex column grow">
        
    <div class="filter-by flex grow wrap">
      <div class="time-filter flex grow">
        <div class="row-button pointer row-button--active align-center">${exercise}</div>
      </div>
    </div>

    <div class="leaderboard-row flex align-center row--header" style="border-radius: 0 !important;">
      <div class="row-position">Position</div>
      <div class="row-collapse flex align-center">
        <div class="row-user--header">Name</div>
      </div>
      <div class="row-calls">Reps</div>
    </div>
  </div>`);
    for (const row of boardData)
    {
        var row_html = `<div class="leaderboard-body flex column grow">
              <div class="leaderboard-row flex align-center">
                <div class="row-position">${count}</div>
                <div class="row-collapse flex align-center">
                  <div class="row-team">${row[0]}</div>
                </div>
                <div class="row-calls">${row[1]}</div>
              </div>
        
            </div>`;
        board.append(row_html);
        board.append(`<div class="leaderboard-footer flex align-center">
        </div>`);
        count += 1;

    }
}


function getAndUpdateLeaderBoards() {
    $.getJSON('/leaderboarddata',
        function(data) {
            console.log(data)
            updateLeaderBoard(data, 'squats');
            updateLeaderBoard(data, 'pushups');
            updateLeaderBoard(data, 'bicepcurls');
        }
    )
}

$(function() {
    var pushups_board = $('pushups');
    var squats_board = $('squats');
    var bicepcurls_board = $('bicepcurls');
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
    setInterval(()=>{
        getAndUpdateLeaderBoards();
    }, 5000);
    function start_exercise(exercise) {
        var name_box = $('#name');

        if (name_box.val().length == 0)
        {
            name_box.addClass('important');
            return false;
        }

        flip_buttons(false);
        exercise();
        return false;
    }
});