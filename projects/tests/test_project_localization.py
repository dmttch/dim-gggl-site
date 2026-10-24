"""
Tests for translated project content rendering.
"""
from html import unescape

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
class TestProjectLocalization:
    def test_should_render_project_content_in_french_when_locale_is_french(
        self,
        client,
        project_factory,
    ):
        """
        Ensure dynamic project fields are translated when French is active.
        """

        project = project_factory()
        client.cookies[settings.LANGUAGE_COOKIE_NAME] = "fr"

        response = client.get(
            reverse("projects:detail", kwargs={"slug": project.slug})
        )

        assert response.status_code == 200
        content = unescape(response.content.decode())

        assert "Projets d'étude" in content
        assert "CRM CLI pour une agence événementielle" in content
        assert "Authentification JWT (SimpleJWT)" in content

    def test_dmttch_projects_have_french_translations_in_catalog(self):
        """
        Ensure newly added @dmttch projects have complete French translations.
        """
        from core.localization.content_catalog import CONTENT_TRANSLATIONS
        from projects.tests.test_projects_json_contract import load_projects

        fr_catalog = CONTENT_TRANSLATIONS["fr"]
        projects_by_slug = {
            project["slug"]: project for project in load_projects()
        }

        for slug in ("gemma-agents", "sceau", "tmd"):
            project = projects_by_slug[slug]
            for field in ("tagline", "description", "challenges", "learnings"):
                value = project.get(field)
                if value:
                    assert value in fr_catalog, (
                        f"Missing FR translation for {slug}.{field}"
                    )
            for feature in project.get("features", []):
                assert feature in fr_catalog, (
                    f"Missing FR translation for feature in {slug}: {feature}"
                )
