FROM golang:1.17

WORKDIR /app
COPY pkg .

ARG GOARCH=amd64
ENV GOARCH=${GOARCH}
ENV GOOS=linux

RUN go mod download
RUN go build -o home

EXPOSE 2112

CMD ["./home"]
