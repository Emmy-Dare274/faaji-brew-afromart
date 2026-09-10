from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class NonStrictManifestStaticFilesStorage(ManifestStaticFilesStorage):

    """ Falls back to the original, unhashed filename instead of
    crashing the whole collectstatic run when a CSS file references
    a static asset that doesn't actually exist on disk. Needed
    because django-countries' packaged sprite-hq.css references a
    PNG that isn't bundled in this release's wheel — harmless for
    us, since AfroMart never renders country flag icons anywhere on
    the site, but Django's manifest storage normally treats *any*
    broken reference as a fatal error regardless of where it comes
    from. manifest_strict only covers a different, later lookup
    path, so the real fix has to catch it here instead. """

    manifest_strict = False

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
