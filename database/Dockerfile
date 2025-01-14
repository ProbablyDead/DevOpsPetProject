FROM golang:1.23.4-alpine AS build-stage

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY src/go.mod src/go.sum ./
RUN go mod download

COPY src/*.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /src

#######
# Run app
#######
FROM alpine

WORKDIR /app

COPY --from=build-stage /src src

# Run
CMD ["./src"]
