/**
 * Created by jmadison on 12/17/14.
 */


console.log("main.js is running now...");

//$(window).load(function () {
//        $('.Collage').collagePlus();
//        console.log("collagiying now....");
//    });




$(".Collage").justifiedGallery({
    randomize: true,
    margins: 2,
    rowHeight: 400,
    lastRow : 'justify',
    fixedHeight: true

}).on('jg.complete', function (e) {
    console.log('on complete');
});
//
//
//console.log("am I doing something? Anything??");
//$("#basic2").justifiedGallery({
//    randomize: true,
//    margins: 2,
//    rowHeight: 400,
//    lastRow : 'justify',
//    fixedHeight: true
//
//}).on('jg.complete', function (e) {
//    console.log('on complete');
//});