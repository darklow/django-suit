'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var autoprefixer = require('gulp-autoprefixer');
var plumber = require('gulp-plumber');

var config = {
    djangoHost: 'localhost',
    djangoPort: 8000,
    jsPort: 8001,
    watchSassFiles: 'suit/sass/**/*.scss',
    cssOutputDir: 'suit/static/suit/css/',
    watchHtmlFiles: [
        'suit/templates/**/*.html',
        'demo/demo/templates/**/*.html'
    ]
};

gulp.task('styles', function () {
    return gulp.src(config.watchSassFiles)
        .pipe(plumber())
        .pipe(sass({outputStyle: 'compact'})).on('error', sass.logError)
        .pipe(autoprefixer({browsers: ['last 2 version', '> 5%']}))
        .pipe(gulp.dest(config.cssOutputDir))
        .pipe(reload({stream: true}))
        ;
});

gulp.task('watch', function () {
    browserSync({
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

    gulp.watch(config.watchSassFiles, ['styles']);
    gulp.watch(config.watchHtmlFiles).on('change', reload);
});

gulp.task('default', ['styles', 'watch']);
