from app.domain.language import LanguagePrediction
from app.domain.ner import EntityLabel, EntityPrediction
from app.models.registry import ModelRegistry
from app.schemas.ner import NERRequest
from app.services.language import LanguageService
from app.services.ner import NERService


class FakeNERModel:
    def predict(self, text: str) -> list[EntityPrediction]:
        return [
            EntityPrediction(
                text="Madrid",
                label=EntityLabel.LOCATION,
                start=13,
                end=19,
                confidence=0.96,
            )
        ]


class FakeLanguageDetector:
    def detect(self, text: str) -> LanguagePrediction:
        return LanguagePrediction(
            code="es",
            confidence=0.98,
        )


def test_ner_service_uses_registry_model():
    registry = ModelRegistry()

    registry.register(
        task="ner",
        language="*",
        factory=FakeNERModel,
    )

    language_service = LanguageService(
        detector=FakeLanguageDetector()
    )

    service = NERService(
        registry=registry,
        language_service=language_service,
    )

    request = NERRequest(
        text="Sara visitó Madrid."
    )

    result = service.analyze(request)

    assert result.language.code == "es"
    assert result.language.confidence == 0.98
    assert len(result.entities) == 1
    assert result.entities[0].text == "Madrid"
    assert result.entities[0].label == EntityLabel.LOCATION
