FROM debian:bookworm
RUN apt-get update && apt-get install -y git curl build-essential clang
RUN git clone --recursive 'https://github.com/cea-sec/hairgap.git' "/tmp/hairgap"
RUN mkdir -p "/tmp/hairgap/include/wirehair"
RUN curl -so "/tmp/hairgap/include/wirehair/wirehair.h" "https://raw.githubusercontent.com/catid/wirehair/master/include/wirehair/wirehair.h"
RUN curl -so "/tmp/hairgap/gf256.h" "https://raw.githubusercontent.com/catid/wirehair/master/gf256.h"
RUN curl -so "/tmp/hairgap/wirehair.cpp" "https://raw.githubusercontent.com/catid/wirehair/master/wirehair.cpp"
RUN curl -so "/tmp/hairgap/gf256.cpp" "https://raw.githubusercontent.com/catid/wirehair/master/gf256.cpp"
RUN cd "/tmp/hairgap/wirehair" && make
RUN cd "/tmp/hairgap" && make

# FROM python:3.10-alpine
# ENV PYTHONUNBUFFERED 1
# #mv "hairgapr" "/vagrant/hairgap_binaries/manylinux2014_x86_64-hairgapr"
# #mv "hairgaps" "/vagrant/hairgap_binaries/manylinux2014_x86_64-hairgaps"
# RUN apk - no-cache update
# RUN apk add --no-cache musl-dev git gcc curl make clang
# RUN git clone --recursive 'https://github.com/cea-sec/hairgap.git' "/tmp/hairgap"
# RUN mkdir -p "/tmp/hairgap/include/wirehair"
# RUN curl -so "/tmp/hairgap/include/wirehair/wirehair.h" "https://raw.githubusercontent.com/catid/wirehair/master/include/wirehair/wirehair.h"
# RUN curl -so "/tmp/hairgap/gf256.h" "https://raw.githubusercontent.com/catid/wirehair/master/gf256.h"
# RUN curl -so "/tmp/hairgap/wirehair.cpp" "https://raw.githubusercontent.com/catid/wirehair/master/wirehair.cpp"
# RUN curl -so "/tmp/hairgap/gf256.cpp" "https://raw.githubusercontent.com/catid/wirehair/master/gf256.cpp"
# RUN cd "/tmp/hairgap/wirehair" && make
# RUN sed -i 's/-Werror/-lstdc++/g' "/tmp/hairgap/GNUmakefile"
# RUN cd "/tmp/hairgap" && make
