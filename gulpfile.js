'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var browsersync = require('browser-sync').create();
var reload = browsersync.reload;
var autoprefixer = require('gulp-autoprefixer');
var plumber = require('gulp-plumber');

var config = {
    djangoHost: 'localhost',
    djangoPort: 8004,
    jsPort: 8005,
    watchSassFiles: 'suit/sass/**/*.scss',
    cssOutputDir: 'suit/static/suit/css/',
    watchHtmlFiles: [
        'suit/templates/**/*.html',
        'demo/demo/templates/**/*.html'
    ]
};

function styles() {
    return gulp.src(config.watchSassFiles)
        .pipe(plumber())
        .pipe(sass({outputStyle: 'compact'})).on('error', sass.logError)
        .pipe(autoprefixer({browsers: ['last 2 version', '> 5%']}))
        .pipe(gulp.dest(config.cssOutputDir))
        .pipe(reload({stream: true}))
        ;
}

// live browser loading
function initBrowserSync(done) {
    browsersync.init({
        port: config.jsPort,
        ui: false,
        notify: false,
        ghostMode: false,
        https: false,
        startPath: '/admin/',
        proxy: {
            target: config.djangoHost + ':' + config.djangoPort
        }
    });
    done();
}

function reloadBrowserSync(done) {
    browsersync.reload();
    // browsersync.stream({once: true})
    done();
}

function watchFiles() {
    gulp.watch(config.watchSassFiles, gulp.series(generateStyles, reloadBrowserSync));
    gulp.watch(config.watchHtmlFiles, gulp.series(reloadBrowserSync));
}

var generateStyles = gulp.parallel(
    gulp.series(styles),
);

var dev = gulp.parallel(
    initBrowserSync,
    watchFiles
);

exports.default = gulp.series(generateStyles, dev)
exports["build"] = generateStyles
exports["dev"] = dev

