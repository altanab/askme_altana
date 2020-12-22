$('.js-vote').click(function (ev){
    ev.preventDefault();
    var $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid'),
        type = $this.data('type');
    $.ajax('/vote/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid,
            type: type
        },
        success: function (data) {
            if (type == "question") {
                var el = '#question_rating_' + qid;
            } else if (type == "answer") {
                var el = '#answer_rating_' + qid;
            }
            $(el).html(data.rating);
        },
        error: function () {
            alert("Log in");
        },
    });
    console.log("working: " + action + " " + qid);
});