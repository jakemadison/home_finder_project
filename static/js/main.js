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



$('#spam_btn').on("click", function() {
    console.log('clicked! --> post: ', POST_ID);

    $.post("delete_post", {'post_id': POST_ID}, function(result) {
        console.log("resulted!", result);
        location.reload(false);
    })
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

$('.refresh_icon').on("click", function() {
   console.log('refresh button has been activated');

    //$.get("refresh_post", function(result) {
    //
    //})

});






$('#next_btn').on("click", function() {
    console.log('clicked!');
    location.reload(false);
});


$.get('get_count', function(data) {

    console.log(data);
    $('.post_count').text(data['post_count']);
    $('.save_count').text(data['save_count']);


});


