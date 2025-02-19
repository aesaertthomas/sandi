import subprocess

adapter_name = "Ethernet"  #Change this to your network adapter name, if you use external adapter (aka hub, you will probably have another name)
static_ip = "192.168.168.10"
subnet_mask = "255.255.255.0"
gateway = "192.168.168.1"
dns1 = "1.1.1.1"
dns2 = "8.8.8.8"

#Disable the usages of dhcp and go to your static IP address
subprocess.run(f'netsh interface ip set address name="{adapter_name}" static {static_ip} {subnet_mask} {gateway}', shell=True)

#Set your DNS servers, (cloudflare and google)
subprocess.run(f'netsh interface ip set dns name="{adapter_name}" static {dns1}', shell=True)
subprocess.run(f'netsh interface ip add dns name="{adapter_name}" {dns2} index=2', shell=True)

print("DHCP disabled and static IP set.")
