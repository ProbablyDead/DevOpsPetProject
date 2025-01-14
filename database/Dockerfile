FROM golang:1.23.4-alpine AS build-stage

# Set destination for COPY
WORKDIR /app

# Download Go modules
ENV GOFLAGS=-work

COPY src/go.mod src/go.sum ./src/
COPY go.work go.work.sum ./
RUN go mod download

COPY src/*.go ./src/

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o ./bin/database ./src/

#######
# Run app
#######
FROM alpine

WORKDIR /app

COPY --from=build-stage /app/bin/database ./bin/database

# Run
CMD ["./bin/database"]
