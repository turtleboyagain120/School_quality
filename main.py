import json
import urllib.request

# ==========================================================
# REPOSITORY: school_quality
# STUDIO:     School Quality Studios
# PRODUCT:    ASCHOOL Tech Protocol
# ADMIN:      <turtleboyagain120>
# ==========================================================

def transmit_to_studio():
    # THE DATA (JSON System Report)
    data_packet = {
        "username": "School Quality Studios Bot",
        "embeds": [{
            "title": "🛰️ SYSTEM SYNC: school-quality",
            "description": "The ASCHOOL Protocol has successfully moved a data node to the Studio.",
            "color": 65535,
            "fields": [
                {"name": "Studio", "value": "School Quality Studios", "inline": True},
                {"name": "Node Admin", "value": "<turtleboyagain120>", "inline": True},
                {"name": "Status", "value": "🟢 OPERATIONAL", "inline": False}
            ],
            "footer": {"text": "Verified: School Quality Studios Engineering"}
        }]
    }

    # YOUR VERIFIED WEBHOOK URL
    WEBHOOK_URL = "https://discord.com/api/webhooks/1499069634337308803/wfrIws-WCioOVMxdso-ipKeWxdQBgW9mUfh5bMfmNH2q5zeKbGZZoiOQH9e_KFGz1I5w"

    try:
        req_data = json.dumps(data_packet).encode('utf-8')
        req = urllib.request.Request(WEBHOOK_URL, data=req_data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', 'Mozilla/5.0')

        with urllib.request.urlopen(req) as response:
            if response.status == 204:
                print("✅ SUCCESS: Data node received at School Quality Studios.")
            else:
                print(f"⚠️ STATUS: {response.status}")
                
    except Exception as e:
        print(f"❌ CRITICAL_FAILURE: {e}")

if __name__ == "__main__":
    transmit_to_studio()
