PIPELINE_CSS = {
    'commoncss': {
        'source_filenames': (
            'css/reset.css',
            'css/themes/*.css',
            'css/jquery.*.css',
            'css/*.css',
        ),
        'output_filename': 'css/common.css',
        'extra_context': {
            'media': 'screen,print',
        },
    },
}

PIPELINE_JS = {
    'commonjs': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery.mobile.min.js',
            'js/*.js',
        ),
        'output_filename': 'js/common.js',
    }
}
