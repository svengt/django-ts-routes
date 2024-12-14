from os import path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils import translation

from ...serializers import url_patterns_serializer


class Command(BaseCommand):
    """Dump Django URLs and the resolver helper to a TS file per language."""

    help = "Dump Django URLs and the resolver helper to a TS file per language."

    def add_arguments(self, parser):
        parser.add_argument(
            "-o",
            "--output-dir",
            required=True,
            help="Specifies a directory to which the output is written.",
        )

    def _write_resolver_file(self, filename):
        result = render_to_string(
            "ts_routes/_dump/resolver.ts",
            {"routes": url_patterns_serializer.to_json()},
        )
        with open(filename, "w") as output:
            output.write(result)

    def handle(self, *args, **options):
        filename = path.join(options["output_dir"], "index.ts")
        self._write_resolver_file(filename)

        for lang, _ in settings.LANGUAGES:
            with translation.override(lang):
                filename = path.join(options["output_dir"], f"{lang}.ts")
                self._write_resolver_file(filename)
