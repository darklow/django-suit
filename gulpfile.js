'use strict';

var sass = require('gulp-sass')(require('sass'));
var sourcemaps = require('gulp-sourcemaps');
var gulp = require('gulp');
var browsersync = require('browser-sync').create();
var reload = browsersync.reload;
var autoprefixer = require('gulp-autoprefixer');
var plumber = require('gulp-plumber');

var config = {
    djangoHost: 'localhost',
    djangoPort: 8003,
    jsPort: 8005,
    watchSassFiles: 'suit/sass/**/*.scss',
    cssOutputDir: 'suit/static/suit/css/',
    jsVendorOutputDir: 'suit/static/vendor/js/',
    cssVendorOutputDir: 'suit/static/vendor/css/',
    watchHtmlFiles: [
        'suit/templates/**/*.html',
        'demo/demo/templates/**/*.html'
    ]
};

function styles() {
    return gulp.src(config.watchSassFiles)
        .pipe(plumber())
        .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'expanded'})).on('error', sass.logError) //expanded or compressed
        .pipe(autoprefixer({ overrideBrowserslist: ['last 2 versions', '>5%'] })) // Adds vendor prefixes
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(config.cssOutputDir))
        .pipe(reload({stream: true}))
        ;
}

function styles_additional() {
	return gulp.src(['node_modules/bootstrap/dist/css/bootstrap-utilities.css',
                     'node_modules/bootstrap/dist/css/bootstrap-utilities.css.map',
	                 'node_modules/bootstrap/dist/css/bootstrap-utilities.min.css',
                     'node_modules/bootstrap/dist/css/bootstrap-utilities.min.css.map'])
		.pipe(gulp.dest(config.cssVendorOutputDir));
}

function scripts() {
	return gulp.src(['node_modules/bootstrap/dist/js/bootstrap.js',
                     'node_modules/bootstrap/dist/js/bootstrap.js.map',
	                 'node_modules/bootstrap/dist/js/bootstrap.min.js',
                     'node_modules/bootstrap/dist/js/bootstrap.min.js.map',
	                 'node_modules/bootstrap/dist/js/bootstrap.bundle.js',
                     'node_modules/bootstrap/dist/js/bootstrap.bundle.js.map',
	                 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
                     'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map'])
		.pipe(gulp.dest(config.jsVendorOutputDir));
}

var generateAssets = gulp.parallel(
    gulp.series(styles_additional, styles, scripts)
);

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
    gulp.watch(config.watchSassFiles, gulp.series(generateAssets, reloadBrowserSync));
    gulp.watch(config.watchHtmlFiles, gulp.series(reloadBrowserSync));
}

var generateStyles = gulp.parallel(
    gulp.series(styles),
);

var dev = gulp.parallel(
    initBrowserSync,
    watchFiles
);

exports.default = gulp.series(generateAssets, dev)
exports["build"] = generateAssets
exports["dev"] = dev

