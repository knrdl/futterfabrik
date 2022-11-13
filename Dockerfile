FROM python:3-alpine

ENV PYTHONIOENCODING=utf-8
ENV PYTHONUNBUFFERED=1

# use fast lxml parser
RUN apk add --no-cache libcap libxslt libxml2

# allow non privileged user to run server on port 80
RUN apk add --no-cache libcap && \
    setcap 'cap_net_bind_service=+ep' "$(readlink -f "$(which python3)")" && \
    apk del libcap

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

