from fastapi import Request


def mark_usage_task(task: str):
    def dependency(request: Request) -> None:
        request.state.usage_task = task

    return dependency


mark_sentiment_usage = mark_usage_task("sentiment")
mark_ner_usage = mark_usage_task("ner")
