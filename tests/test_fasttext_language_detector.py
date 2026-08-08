from app.models.adapters.language.fasttext_detector import (
    FastTextLanguageDetector,
)


class FakeFastTextModel:
    def __init__(self, label: str, confidence: float):
        self.label = label
        self.confidence = confidence

    def predict(self, text: str, k: int = 1):
        return (
            [self.label],
            [self.confidence],
        )


def test_detector_normalizes_fasttext_label():
    detector = FastTextLanguageDetector(
        model=FakeFastTextModel(
            "__label__es",
            0.987654,
        )
    )

    result = detector.detect("Me encantó este producto.")

    assert result.code == "es"
    assert result.confidence == 0.9877


def test_detector_returns_english():
    detector = FastTextLanguageDetector(
        model=FakeFastTextModel(
            "__label__en",
            0.95,
        )
    )

    result = detector.detect("This product is great.")

    assert result.code == "en"
    assert result.confidence == 0.95


def test_detector_removes_newlines_before_prediction():
    class RecordingModel:
        def __init__(self):
            self.received_text = None

        def predict(self, text: str, k: int = 1):
            self.received_text = text
            return (
                ["__label__es"],
                [0.99],
            )

    model = RecordingModel()

    detector = FastTextLanguageDetector(model=model)

    detector.detect("Hola\n¿Cómo estás?")

    assert model.received_text == "Hola ¿Cómo estás?"
