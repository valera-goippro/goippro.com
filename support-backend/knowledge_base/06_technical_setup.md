# Technical Setup Guide

## GoIP Device Configuration

### Step 1: Physical Setup
1. Unbox your GoIP device
2. Insert SIM cards into SIM slots
3. Connect ethernet cable from GoIP to your router/switch
4. Connect power adapter
5. Wait 2-3 minutes for device to boot

### Step 2: Access GoIP Web Interface
1. Find your GoIP's IP address (check your router's DHCP clients list)
2. Default IP is often 192.168.8.1 or assigned by DHCP
3. Open browser and go to http://<GoIP-IP>
4. Default login: admin / admin
5. Change password immediately after first login!

### Step 3: SIP Configuration
1. Go to Configuration → SIP Settings
2. Set SIP Server: provided by GoIPPro support after registration
3. Set SIP Port: as provided
4. Set Authentication ID: your assigned channel ID
5. Set Password: your assigned SIP password
6. Save and apply

### Step 4: Verify Connection
1. Check SIM card status — all slots should show "registered"
2. SIP status should show "registered" or "online"
3. Your channels will appear in GoIPPro dashboard
4. 10-day validation period begins automatically

## Network Requirements
- Static IP is preferred but not required
- If behind NAT: ensure SIP ALG is DISABLED on your router
- Port forwarding may be needed: SIP (5060/UDP), RTP (10000-20000/UDP)
- Or use our MikroTik VPN setup for seamless connectivity

## MikroTik VPN Setup (Recommended)
- We provide a MikroTik RouterOS script for WireGuard VPN
- This creates a direct tunnel from your GoIP to our server
- Benefits: no port forwarding, no NAT issues, stable connection
- Ask support for the MikroTik enrollment script

## Firewall Considerations
- GoIP needs outbound access to our SIP server
- If using VPN: only WireGuard port needs to be open (UDP)
- No inbound ports needed if using VPN tunnel
