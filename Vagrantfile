Vagrant.configure("2") do |config|
    config.vm.define "centos_8" do |centos_8|
        centos_8.vm.box = "centos/8"
        centos_8.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
        centos_8.vm.provision "shell", path: "compile.sh"
    end
    config.vm.define "debian_9" do |debian_9|
        debian_9.vm.box = "debian/stretch64"
        debian_9.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
    end
end
