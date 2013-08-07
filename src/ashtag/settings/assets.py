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
    'jquery': {
        'source_filenames': (
            'js/lib/jquery-1.9.1.min.js',
            'js/lib/jquery.mobile-1.3.1.min.js',
        ),
        'output_filename': 'js/jquery.js',
    },
    'commonjs': {
        'source_filenames': (
            'js/jquery.min.js',
            'js/jquery.mobile.min.js',
            'js/*.js',

            'compiled-js/lib/panes.js',
            'compiled-js/lib/*.js',
            'compiled-js/panes/map-base.js',
            'compiled-js/panes/*.js',
            'compiled-js/*.js',
        ),
        'output_filename': 'js/common.js',
    }
}

# Checkout apps/core/__init__.py for some pipeline monkeypatching
