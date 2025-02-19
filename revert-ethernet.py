import subprocess

adapter_name="Ethernet"
subprocess.run(f'netsh interface ip set address name="{adapter_name}" dhcp', shell=True, check=True)
subprocess.run(f'netsh interface ip set dns name="{adapter_name}" dhcp', shell=True, check=True)
print(f"DHCP enabled and static IP reverted for {adapter_name}.")
