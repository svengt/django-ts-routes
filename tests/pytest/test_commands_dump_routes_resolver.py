import tempfile
from os import path

from django.core.management import call_command
from django.template.loader import render_to_string
from django.test.testcases import SimpleTestCase, override_settings
from django.utils import translation

from ts_routes.serializers import url_patterns_serializer


class TestDumpRoutesResolverCommand(SimpleTestCase):
    @override_settings(LANGUAGES=[("en", "English")])
    def test_can_export_the_routes_and_resolver_module_into_a_specific_directory(self):
        export_dir = tempfile.mkdtemp()
        call_command("dump_routes_resolver", output_dir=export_dir)

        index_filename = path.join(export_dir, "index.ts")
        en_filename = path.join(export_dir, "en.ts")
        nl_filename = path.join(export_dir, "nl.ts")

        assert path.exists(index_filename)
        assert path.exists(en_filename)
        assert not path.exists(nl_filename)

        result = render_to_string(
            "ts_routes/_dump/resolver.ts", {"routes": url_patterns_serializer.to_json()}
        )

        with open(index_filename) as fd:
            assert fd.read() == result

        with open(en_filename) as fd:
            assert fd.read() == result

    @override_settings(LANGUAGES=[("en", "English"), ("nl", "Dutch")])
    def test_can_export_the_routes_and_resolver_module_into_a_specific_directory_languages(
        self,
    ):
        export_dir = tempfile.mkdtemp()
        call_command("dump_routes_resolver", output_dir=export_dir)

        index_filename = path.join(export_dir, "index.ts")
        en_filename = path.join(export_dir, "en.ts")
        nl_filename = path.join(export_dir, "nl.ts")

        assert path.exists(index_filename)
        assert path.exists(en_filename)
        assert path.exists(nl_filename)

        with translation.override("en"):
            result = render_to_string(
                "ts_routes/_dump/resolver.ts",
                {"routes": url_patterns_serializer.to_json()},
            )

            with open(index_filename) as fd:
                assert fd.read() == result

            with open(en_filename) as fd:
                assert fd.read() == result

            with open(nl_filename) as fd:
                assert fd.read() != result, result

        with translation.override("nl"):
            result = render_to_string(
                "ts_routes/_dump/resolver.ts",
                {"routes": url_patterns_serializer.to_json()},
            )

            with open(index_filename) as fd:
                assert fd.read() != result

            with open(en_filename) as fd:
                assert fd.read() != result

            with open(nl_filename) as fd:
                assert fd.read() == result
