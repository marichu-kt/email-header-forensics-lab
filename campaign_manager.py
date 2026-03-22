import json
import os
import datetime

class CampaignManager:
    def __init__(self, campaigns_dir='campaigns'):
        self.campaigns_dir = campaigns_dir
        self.campaigns_file = os.path.join(campaigns_dir, 'campaigns.json')
        os.makedirs(campaigns_dir, exist_ok=True)
        self.campaigns = self.load_campaigns()

    def load_campaigns(self):
        if os.path.exists(self.campaigns_file):
            try:
                with open(self.campaigns_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_campaigns(self):
        with open(self.campaigns_file, 'w', encoding='utf-8') as f:
            json.dump(self.campaigns, f, indent=2, ensure_ascii=False)

    def save_template(self, name, headers):
        self.campaigns[name] = {
            'headers': headers,
            'created': datetime.datetime.now().isoformat()
        }
        self.save_campaigns()

    def load_template(self, name):
        return self.campaigns.get(name, {}).get('headers', [])

    def list_templates(self):
        return list(self.campaigns.keys())

    def delete_template(self, name):
        if name in self.campaigns:
            del self.campaigns[name]
            self.save_campaigns()
            return True
        return False