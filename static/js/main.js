/**
 * Created by jmadison on 12/17/14.
 */


console.log("am I doing something? Anything??");
$("#basicExample").justifiedGallery({
    randomize: true,
    margins: 2,
    rowHeight: 400,
    lastRow : 'justify',
    fixedHeight: true

}).on('jg.complete', function (e) {
    console.log('on complete');
});


console.log("am I doing something? Anything??");
$("#basic2").justifiedGallery({
    randomize: true,
    margins: 2,
    rowHeight: 400,
    lastRow : 'justify',
    fixedHeight: true

}).on('jg.complete', function (e) {
    console.log('on complete');
});