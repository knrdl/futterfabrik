FROM alpine

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache python3 py3-beautifulsoup4 py3-requests py3-lxml py3-jinja2 libcap && \
    setcap 'cap_net_bind_service=+ep' "$(readlink -f "$(which python3)")" && \
    apk del libcap

COPY src /app

EXPOSE 80/tcp

RUN adduser --no-create-home --disabled-password --shell /bin/false --uid 1000 futterfabrik

WORKDIR /app

USER futterfabrik

CMD python3 .
