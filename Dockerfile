FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install CPU-only PyTorch first so the image does not pull GPU/CUDA packages.
RUN python -m pip install --upgrade pip \
    && python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

COPY pyproject.toml README.md ./
COPY app ./app
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic

RUN python -m pip install .

# Download the lightweight fastText language-ID model.
RUN mkdir -p resources/models \
    && python -c "import urllib.request; urllib.request.urlretrieve('https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz', 'resources/models/lid.176.ftz')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
