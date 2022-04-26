FROM python:3-slim

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

# allow non privileged user to run server on port 80
RUN apt-get update && \
    apt-get install -y --no-install-recommends libcap2-bin && \
    setcap 'cap_net_bind_service=+ep' "$(readlink -f "$(which python3)")" && \
    apt-get purge libcap2-bin && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --home /home/futterfabrik --disabled-password --shell /bin/false --uid 1000 futterfabrik
ENV PATH "/home/futterfabrik/.local/bin:$PATH"

CMD python3 .

EXPOSE 80/tcp

WORKDIR /app

USER futterfabrik

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src .

