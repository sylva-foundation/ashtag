# -*- mode: ruby -*-
# vi: set ft=ruby :

# Based on vagrant-django-template here:
#   https://github.com/torchbox/vagrant-django-template

Vagrant::Config.run do |config|
    
    config.vm.box = "ashtag64"
    config.vm.box_url = "https://dl.dropboxusercontent.com/u/41936/ashtag64.box"

    # If you wish you can use the precise64 box instead. The build will 
    # take longer, but it may save you a large download.
    # config.vm.box = "precise64"
    # config.vm.box_url = "http://files.vagrantup.com/precise64.box"
    
    # Boot with a GUI so you can see the screen. (Default is headless)
    # config.vm.boot_mode = :gui
    
    # Assign this VM to a host only network IP, allowing you to access it
    # via the IP.
    # config.vm.network "33.33.33.10"
    
    # Make the Django dev server available to the host machine on 8080.
    config.vm.forward_port 8080, 8080
    
    # Share an additional folder to the guest VM. The first argument is
    # an identifier, the second is the path on the guest to mount the
    # folder, and the third is the path on the host to the actual folder.
    config.vm.share_folder "project", "/home/vagrant/ashtag", "."
    
    # Enable provisioning with a shell script.
    config.vm.provision :shell, :path => "vagrant/install/install.sh", :args => "ashtag"
end
