$script_master = <<-SCRIPT
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
sudo apt update
sudo apt install -y net-tools
sudo apt install -y network-manager
sudo apt install -y isc-dhcp-server
sudo apt install -y iperf
sudo cp /vagrant/dhcpd.conf /etc/dhcp/
sudo chmod 666 /var/lib/dhcp/dhcpd.leases
sudo dhcpd
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o enp0s3 -s 10.0.0.0/24 -j MASQUERADE
sudo DEBIAN_FRONTEND=noninteractive apt install -y tshark
SCRIPT

$script_slave = <<-SCRIPT
sudo apt update
sudo apt install -y iperf
sudo ip route del default via 10.0.2.2 dev enp0s3
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.define "master" do |master|
      master.vm.box = "ubuntu/jammy64"
      master.vm.box_version = "20240912.0.0"
      master.vm.hostname = "master"
      master.vm.provision "shell", inline: $script_master
      master.vm.network "private_network", ip: "10.0.0.1",
        virtualbox__intnet: "mynetwork"
    end
    config.vm.define "slave" do |slave|
      slave.vm.box = "ubuntu/jammy64"
      slave.vm.box_version = "20240912.0.0"
      slave.vm.hostname = "slave"
      slave.vm.network "private_network", type: "dhcp",
        virtualbox__intnet: "mynetwork"
      slave.vm.provision "shell", inline: $script_slave
    end
end


