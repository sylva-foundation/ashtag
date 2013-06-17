PIPELINE_CSS = {
    'commoncss': {
        'source_filenames': (
            'css/reset.css',
            'cookielaw/css/cookielaw.css',
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
            'js/*.js',
            'cookielaw/js/cookielaw.js',
        ),
        'output_filename': 'js/common.js',
    }
}
