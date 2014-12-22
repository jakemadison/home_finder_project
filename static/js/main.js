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
