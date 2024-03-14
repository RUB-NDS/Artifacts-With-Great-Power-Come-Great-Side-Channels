FROM alpine:3.19.1

# Proxy dependencies
RUN apk add --no-cache clang libpcap-dev cmake boost boost-dev
# TLS-Docker-Timer dependencies
RUN apk add --no-cache openjdk11 openjdk11-jre maven git 
# TLS-Docker-Library dependencies
RUN apk add --no-cache bash docker-cli-buildx python3 make go 

# Clone and build proxy
RUN git clone --depth 1 --branch v1.0.0 https://github.com/tls-attacker/Timing-Proxy.git
WORKDIR /Timing-Proxy/
# Fix proxy compile for C++ headers
RUN find . \( -name "*.cpp" -o -name "*.h" \) -exec sed -i -e 's/u_char/uint8_t/g' -e 's/u_int16_t/uint16_t/g' -e 's/u_int8_t/uint8_t/g' {} +
RUN mkdir build/
WORKDIR /Timing-Proxy/build 
RUN cmake -G "Unix Makefiles" ..
RUN make

# Clone docker library
RUN git clone --depth 1 --branch v2.3.1 https://github.com/tls-attacker/TLS-Docker-Library.git /TLS-Docker-Library/
WORKDIR /TLS-Docker-Library/
# Allow caching to speed up builds for additional images
RUN sed -i 's/--no-cache//g' ./images/baseimage/build-base-image.sh


# Clone and build measurement tool
WORKDIR /
RUN git clone --depth 1 --branch v1.0.3 https://github.com/tls-attacker/TLS-Docker-Timer.git
WORKDIR /TLS-Docker-Timer
RUN mvn clean package

COPY entrypoint.sh /entrypoint/
COPY loopProxy.sh /entrypoint/
COPY evalCerts/ /entrypoint/evalCerts/
WORKDIR /entrypoint/
ENTRYPOINT [ "ash", "-i", "entrypoint.sh" ]
