/**
 * Created by jmadison on 12/17/14.
 */


console.log("main.js is running now...");


$(".Collage").justifiedGallery({
    randomize: true,
    margins: 2,
    rowHeight: 200,
    //lastRow : 'hide',
    captions: false
    //fixedHeight: true

}).on('jg.complete', function (e) {
    console.log('on complete');
});


$('.rating_btn').on("click", function() {
    console.log('clicked! --> post: ', POST_ID);

    var rating_type;

    if (this.id == 'like_btn') {
        rating_type = 'like';
    }
    else {
        rating_type = 'dislike';
    }

    $.post("rate_post", {'post_id': POST_ID, 'rating_type': rating_type}, function(result) {
        console.log("resulted!", result);
        location.reload(false);
    })
});


$('#next_btn').on("click", function() {
    console.log('clicked!');
    location.reload(false);
});