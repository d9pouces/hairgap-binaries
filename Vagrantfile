Vagrant.configure("2") do |config|
    config.vm.define "centos_8" do |centos_8|
        centos_8.vm.box = "centos/8"
        centos_8.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
        centos_8.vm.provision "shell", path: "compile.sh"
    end
    config.vm.define "centos_7" do |centos_7|
        centos_7.vm.box = "centos/7"
        centos_7.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
    config.vm.define "debian_9" do |debian_9|
        debian_9.vm.box = "debian/stretch64"
        debian_9.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
    config.vm.define "ubuntu_xenial" do |ubuntu_xenial|
        ubuntu_xenial.vm.box = "ubuntu/xenial64"
        ubuntu_xenial.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
    config.vm.define "ubuntu_bionic" do |ubuntu_bionic|
        ubuntu_bionic.vm.box = "ubuntu/bionic64"
        ubuntu_bionic.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
    config.vm.define "ubuntu_focal" do |ubuntu_focal|
        ubuntu_focal.vm.box = "ubuntu/focal64"
        ubuntu_focal.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
end
