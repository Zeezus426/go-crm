FROM python:3.12.9

WORKDIR /app

COPY requirements.txt .

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./super_researcher /app


CMD ["adk", "run", "SuperResearcher", "I am a medical supply company called gosupply. I sell nutricia and avanos products. These brands focus on producing enteral feeding products. Refine a target market for these products and find customers. More specifically for customers I want you to research for customers like aged care hospitals anyone that would otherwise need nutricia and avanos. I would like these organizations details like emails, addresses and phone numbers."]