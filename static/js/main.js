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


$('#like_btn').on("click", function() {
    console.log('clicked! --> post: ');
    $.post("/like_post", function(result) {
        console.log("resulted!", result);
        location.reload(false);
    })
});


$('#next_btn').on("click", function() {
    console.log('clicked!');
    location.reload(false);

});