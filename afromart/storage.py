from whitenoise.storage import CompressedManifestStaticFilesStorage


class ForgivingManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Some of Django's own bundled admin static files reference an
    icon that isn't shipped with this admin theme, a gap
    in Django's own files, not the code. manifest_strict can only be
    disabled by subclassing directly, per Django's own documentation,
    a settings variable alone does not reliably do this. With it set
    to False here, a missing referenced file is left as a plain,
    unhashed link instead of failing the entire deploy over it."""
    manifest_strict = False