FROM python:3.12-slim
WORKDIR /root
COPY . ./api/
RUN pip install --upgrade pip \
    && pip install virtualenv \
    && python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN . /venv/bin/activate \
    && pip install --no-cache-dir -r ./api/requirements.txt
