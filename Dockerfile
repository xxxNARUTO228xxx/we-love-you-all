FROM ubuntu:latest
LABEL authors="storonkin"

ENTRYPOINT ["top", "-b"]