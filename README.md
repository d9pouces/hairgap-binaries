# hairgap-binaries

Provide compiled binaries of [hairgap](https://github.com/cea-sec/hairgap) under the form of a Python package.

## building 

requirements:
* python3 (>= 3.5),
* wheel (in the current virtualenv),
* vagrant with the scp plugin.

```bash
# install the scp plugin
vagrant plugin install vagrant-scp

# compile binaries in a Vagrant box 
vagrant up centos_8
vagrant scp centos_8:/tmp/hairgap/hairgaps hairgap_binaries/manylinux2014_x86_64-hairgaps
vagrant scp centos_8:/tmp/hairgap/hairgapr hairgap_binaries/manylinux2014_x86_64-hairgapr
vagrant destroy centos_8 --force

# check these binaries on a Debian 9 / CentOS 7 / Xenial / Bionic / Focal 
for k in centos_7 debian_9 ubuntu_xenial ubuntu_bionic ubuntu_focal; do
    vagrant up $k > /dev/null 2> /dev/null && \
    vagrant scp hairgap_binaries/manylinux2014_x86_64-hairgaps $k:/tmp/hairgaps > /dev/null 2> /dev/null && \
    vagrant scp hairgap_binaries/manylinux2014_x86_64-hairgapr $k:/tmp/hairgapr > /dev/null 2> /dev/null && \
    vagrant ssh $k -c "/tmp/hairgaps -h" 2> /dev/null | grep sender > /dev/null && echo "$k : hairgaps valid" && \
    vagrant ssh $k -c "/tmp/hairgapr -h" 2> /dev/null | grep receiver > /dev/null && echo "$k : hairgapr valid" && \
    vagrant destroy --force $k > /dev/null 2> /dev/null
done

# generate Python packages
python3 setup.py sdist
python3 setup.py bdist_wheel -p manylinux2014_x86_64
```
