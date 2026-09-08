from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class NonStrictManifestStaticFilesStorage(ManifestStaticFilesStorage):

    """ Identical to Django's default manifest storage, except a
    file referenced inside a CSS url() that can't be found during
    collectstatic's hashing pass logs a warning instead of crashing
    the whole build. Needed because django-countries' packaged
    sprite-hq.css references a PNG that isn't actually bundled in
    this release, since AfroMart never renders
    country flag icons anywhere on the site. """

    manifest_strict = False