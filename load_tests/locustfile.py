import os

from locust import HttpUser, between, task


API_KEY = os.getenv("POLYTEXT_API_KEY")


class PolyTextUser(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        if not API_KEY:
            raise RuntimeError(
                "POLYTEXT_API_KEY must be set"
            )

        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

    @task(4)
    def spanish_sentiment(self):
        self.client.post(
            "/v1/sentiment",
            headers=self.headers,
            json={
                "text": "Me encanta este producto.",
                "language": "es",
            },
            name="/v1/sentiment [es]",
        )

    @task(2)
    def english_sentiment(self):
        self.client.post(
            "/v1/sentiment",
            headers=self.headers,
            json={
                "text": "I really enjoyed this product.",
                "language": "en",
            },
            name="/v1/sentiment [en]",
        )

    @task(2)
    def entities(self):
        self.client.post(
            "/v1/entities",
            headers=self.headers,
            json={
                "text": (
                    "Sara works at Microsoft "
                    "and recently visited Madrid."
                ),
                "language": "en",
            },
            name="/v1/entities",
        )

    @task(2)
    def classification(self):
        self.client.post(
            "/v1/classify",
            headers=self.headers,
            json={
                "text": (
                    "Apple announced a new "
                    "processor for its laptops."
                ),
                "candidate_labels": [
                    "technology",
                    "sports",
                    "politics",
                    "finance",
                ],
                "language": "en",
            },
            name="/v1/classify",
        )
