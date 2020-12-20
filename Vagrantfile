Vagrant.configure("2") do |config|
    config.vm.define "debian_9" do |debian_9|
        debian_9.vm.box = "debian/stretch64"
        debian_9.vm.provider "virtualbox" do |v|
            v.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
        end
        debian_9.vm.provision "ansible" do |ansible|
            ansible.compatibility_mode = "2.0"
            ansible.playbook = "vagrant.yml"
            ansible.host_vars = {
                "debian_9" => {
                    "ansible_ssh_pipelining" => "true",
                    "ansible_python_interpreter" => "/usr/bin/python3",
                    "platform" => "manylinux1_x86_64",
                },
            }
        end
    end
end
