#!/usr/bin/env bash
rm -rf "/tmp/hairgap"
echo "Install required packages"
yum check-update
yum install -y "@Development Tools" "ca-certificates" "clang" "git"
echo "Download Hairgap"
git clone --recursive 'https://github.com/cea-sec/hairgap.git' "/tmp/hairgap"
mkdir -p "/tmp/hairgap/include/wirehair"
echo "Download wirehair"
for k in "include/wirehair/wirehair.h" "gf256.h" "wirehair.cpp" "gf256.cpp"; do
  curl -so "/tmp/hairgap/$k" "https://raw.githubusercontent.com/catid/wirehair/master/$k"
done
echo "Make wirehair"
cd "/tmp/hairgap/wirehair" || exit 1
make
echo "Make hairgap"
cd "/tmp/hairgap" || exit 1
make
