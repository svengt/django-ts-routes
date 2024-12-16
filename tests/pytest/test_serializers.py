import json

from django.test.testcases import SimpleTestCase, override_settings

from ts_routes.serializers import URLPatternsSerializer


class TestURLPatternsSerializer(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.serializer = URLPatternsSerializer()

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping",
        ]
    )
    def test_can_serialize_specific_urls_that_do_not_have_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping"] == "/ping/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_args",
        ]
    )
    def test_can_serialize_specific_urls_that_have_unnamed_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_args"] == "/ping/<>/foo/<>/bar/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_kwargs",
        ]
    )
    def test_can_serialize_specific_urls_that_have_named_arguments(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_kwargs"] == "/ping/<pk1>/foo/<pk2>/bar/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_optional_character",
        ]
    )
    def test_can_serialize_specific_urls_that_have_optional_characters(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_optional_character"] == "/ping/<>/foo/bar/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_optional_group",
        ]
    )
    def test_can_serialize_specific_urls_that_have_an_optional_group(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_optional_group"] == "/ping/<>/foo/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_optional_kwarg",
        ]
    )
    def test_can_serialize_specific_urls_that_have_an_optional_kwarg(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_optional_kwarg"] == "/ping/<>/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "included_test_with_args",
        ]
    )
    def test_can_serialize_specific_urls_that_have_been_included(self):
        output_dict = json.loads(self.serializer.to_json())
        assert (
            output_dict["included_test_with_args"]
            == "/included/<pk1>/test/<>/foo/<>/bar/"
        )

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_re_path",
        ]
    )
    def test_can_serialize_specific_urls_that_have_a_regex_path(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_re_path"] == "/ping/<year>/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_path",
        ]
    )
    def test_can_serialize_specific_urls_that_have_a_path_expression(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_path"] == "/ping/<int:year>/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_paths",
        ]
    )
    def test_can_serialize_specific_urls_that_have_multiple_path_expressions(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_paths"] == "/ping/<int:year>/<int:month>/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_with_path_without_converter",
        ]
    )
    def test_can_serialize_specific_urls_that_have_a_path_without_converter(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_with_path_without_converter"] == "/ping/<slug>/"

    @override_settings(
        TS_ROUTES_INCLUSION_LIST=[
            "ping_i18n",
        ]
    )
    def test_can_serialize_specific_urls_that_do_not_have_arguments_with_i18n(self):
        output_dict = json.loads(self.serializer.to_json())
        assert output_dict["ping_i18n"] == "/en/ping-i18n/", output_dict
