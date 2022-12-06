'use strict';

const gulp = require('gulp');
const sass = require('gulp-sass');
const browserSync = require('browser-sync');
const autoprefixer = require('gulp-autoprefixer');
const plumber = require('gulp-plumber');
let reload = browserSync.reload;

const config = {
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

    gulp.watch(config.watchSassFiles, gulp.series('styles'));
    gulp.watch(config.watchHtmlFiles).on('change', reload);
});

gulp.task('default', gulp.series('styles', 'watch'));
