# hairgap-binaries

Provide compiled binaries of https://github.com/cea-sec/hairgap


## building 

python3 (>= 3.5), wheel (in the current virtualenv), vagrant with the scp plugin are required.

```bash
# install the scp plugin
vagrant plugin install vagrant-scp

# compile binaries in a Vagrant box 
vagrant up centos_8
vagrant scp centos_8:/tmp/hairgap/hairgaps hairgap_binaries/manylinux1_x86_64-hairgaps
vagrant scp centos_8:/tmp/hairgap/hairgapr hairgap_binaries/manylinux1_x86_64-hairgapr
vagrant destroy centos_8 --force

# check binaries on a Debian 9
vagrant up debian_9
vagrant scp hairgap_binaries/manylinux1_x86_64-hairgaps debian_9:/tmp/hairgaps
vagrant scp hairgap_binaries/manylinux1_x86_64-hairgapr debian_9:/tmp/hairgapr
vagrant ssh debian_9 -c "/tmp/hairgaps -h" 
vagrant ssh debian_9 -c "/tmp/hairgapr -h" 

# generate Python packages
python3 setup.py sdist
python3 setup.py bdist_wheel -p manylinux2014_x86_64
```
