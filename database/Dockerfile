FROM golang:1.23.4-alpine AS build-stage

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY database/go.mod database/go.sum ./
RUN go mod download

COPY src/*.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /database

#######
# Run app
#######
FROM alpine

WORKDIR /app

COPY --from=build-stage /database database

EXPOSE 8001

# Run
CMD ["./database"]
