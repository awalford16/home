FROM golang:1.20

WORKDIR /app
COPY pkg .

RUN go mod download
RUN go build -o home

EXPOSE 2112

CMD ["./home"]
