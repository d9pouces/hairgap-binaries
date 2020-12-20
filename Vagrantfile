Vagrant.configure("2") do |config|
    config.vm.define "centos_8" do |centos_8|
        centos_8.vm.box = "centos/8"
        centos_8.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
        centos_8.vm.provision "ansible" do |ansible|
            ansible.compatibility_mode = "2.0"
            ansible.playbook = "vagrant.yml"
            ansible.host_vars = {
                "centos_8" => {
                    "ansible_ssh_pipelining" => "true",
                    "ansible_python_interpreter" => "/usr/bin/python2.7",
                    "platform" => "manylinux2014_x86_64",
                },
            }
        end
    end
end
