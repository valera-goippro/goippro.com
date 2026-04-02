# Troubleshooting

## SIM Card Issues

### SIM shows "not registered" or "no signal"
- Check SIM is properly inserted (gold contacts facing correct direction)
- Try the SIM in a regular phone to verify it works
- Check if SIM has expired or needs top-up
- Move GoIP device closer to a window for better signal
- Try a SIM from a different operator

### SIM got blocked
- This is rare with inbound-only traffic
- Replace the SIM with a new one
- Notify support so we can update your channel config
- If multiple SIMs get blocked, contact support — there may be an issue

## Connection Issues

### GoIP shows "SIP not registered"
- Verify SIP server address is correct
- Check internet connection (can you ping 8.8.8.8 from GoIP?)
- Ensure SIP ALG is DISABLED on your router
- If behind NAT, try our MikroTik VPN solution
- Check username/password match what support provided
- Restart GoIP device

### No traffic / no calls coming in
- Is your channel past the 10-day validation period?
- Check dashboard — is your channel status "Active"?
- Verify device is online and SIP is registered
- Some markets have variable demand — traffic volume fluctuates
- Contact support if no traffic for 48+ hours after activation

### Poor voice quality
- Check internet stability — run a speed test
- Use wired ethernet, not WiFi
- Ensure no bandwidth-heavy activities on same network
- Check for packet loss: ping our server, look for drops
- Minimum 1 Mbps per 8 ports of stable upload

## Device Issues

### GoIP web interface not accessible
- Check ethernet cable connection
- Try different browser
- Reset GoIP to factory defaults (hold reset button 10 seconds)
- Check if GoIP IP changed (look in router DHCP list)

### GoIP device rebooting frequently
- Check power supply — use original adapter
- Check for overheating — ensure ventilation
- Update firmware if available
- Contact support with device model and symptoms

## Payment Issues

### Haven't received payment
- Check minimum payout threshold ($10)
- Verify your wallet address is correct in dashboard
- Payments are processed monthly
- Check TRC-20/ERC-20 network matches your wallet
- Contact support with your partner ID

## Still Need Help?
- Telegram: @goippro_support
- Email: support@goippro.com
- WhatsApp: available on website
- Response time: typically within 2-4 hours
