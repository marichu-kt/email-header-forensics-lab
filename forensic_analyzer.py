import re
import ipaddress
from email.utils import parsedate_to_datetime

class ForensicAnalyzer:
    def __init__(self, headers):
        self.headers = headers
        self.results = []

    def analyze(self):
        self.check_required_headers()
        self.check_message_id_vs_from()
        self.check_received_ips()
        self.check_dates_order()
        self.check_authentication_results()
        self.check_x_mailer()
        return self.results

    def add_result(self, check_name, status, message):
        self.results.append({
            'check': check_name,
            'status': status,
            'message': message
        })

    def check_required_headers(self):
        headers_dict = dict(self.headers)
        missing = []
        for r in ['Message-ID', 'Date', 'From']:
            if r not in headers_dict:
                missing.append(r)
        if missing:
            self.add_result('Required headers', 'FAIL', f"Missing: {', '.join(missing)}")
        else:
            self.add_result('Required headers', 'PASS', 'All required headers present')

    def check_message_id_vs_from(self):
        headers_dict = dict(self.headers)
        msg_id = headers_dict.get('Message-ID', '')
        from_addr = headers_dict.get('From', '')
        if from_addr and msg_id:
            dominio_from = re.search(r'@([^>]+)', from_addr)
            dominio_msgid = re.search(r'@([^>]+)', msg_id)
            if dominio_from and dominio_msgid:
                if dominio_from.group(1) not in dominio_msgid.group(1) and 'mail.gmail.com' not in dominio_msgid.group(1):
                    self.add_result('Message-ID vs From', 'FAIL', f"Domain mismatch: From domain '{dominio_from.group(1)}' vs Message-ID domain '{dominio_msgid.group(1)}'")
                else:
                    self.add_result('Message-ID vs From', 'PASS', 'Domains are consistent')
            else:
                self.add_result('Message-ID vs From', 'WARN', 'Could not parse domains')
        else:
            self.add_result('Message-ID vs From', 'WARN', 'Missing Message-ID or From')

    def check_received_ips(self):
        private_ips = []
        for name, value in self.headers:
            if name.lower() == 'received':
                ips = re.findall(r'\[(\d+\.\d+\.\d+\.\d+)\]', value)
                for ip in ips:
                    try:
                        ip_obj = ipaddress.ip_address(ip)
                        if ip_obj.is_private:
                            private_ips.append(ip)
                    except:
                        continue
        if private_ips:
            self.add_result('Received IPs', 'FAIL', f"Private IPs found: {', '.join(set(private_ips))}")
        else:
            self.add_result('Received IPs', 'PASS', 'No private IPs detected')

    def check_dates_order(self):
        dates = []
        for name, value in self.headers:
            if name.lower() == 'received':
                match = re.search(r';\s*(.+?)(?:\s*[+-]\d{4})?$', value)
                if match:
                    try:
                        dt = parsedate_to_datetime(match.group(1))
                        dates.append(('received', dt))
                    except:
                        pass
            elif name.lower() == 'date':
                try:
                    dt = parsedate_to_datetime(value)
                    dates.append(('date', dt))
                except:
                    pass
        if len(dates) < 2:
            self.add_result('Date order', 'WARN', 'Not enough dates to compare')
            return
        dates_sorted = sorted(dates, key=lambda x: x[1], reverse=True)
        if dates_sorted[0][0] != 'received' or (len(dates_sorted) > 1 and dates_sorted[1][0] != 'received'):
            self.add_result('Date order', 'FAIL', 'Received headers are not in correct chronological order')
        else:
            self.add_result('Date order', 'PASS', 'Received headers appear in correct order')

    def check_authentication_results(self):
        headers_dict = dict(self.headers)
        auth = headers_dict.get('Authentication-Results', '')
        if not auth:
            self.add_result('Authentication', 'WARN', 'No Authentication-Results header found')
            return
        fails = []
        if 'spf=fail' in auth:
            fails.append('SPF fail')
        if 'dkim=fail' in auth:
            fails.append('DKIM fail')
        if 'dmarc=fail' in auth:
            fails.append('DMARC fail')
        if fails:
            self.add_result('Authentication', 'FAIL', f"Authentication failures: {', '.join(fails)}")
        else:
            self.add_result('Authentication', 'PASS', 'SPF/DKIM/DMARC appear valid')

    def check_x_mailer(self):
        headers_dict = dict(self.headers)
        xm = headers_dict.get('X-Mailer', '')
        if xm:
            known = ['Outlook', 'Thunderbird', 'Apple Mail', 'iPhone', 'Android', 'Gmail']
            if any(k in xm for k in known):
                self.add_result('X-Mailer', 'PASS', f"X-Mailer: {xm} (common)")
            else:
                self.add_result('X-Mailer', 'WARN', f"Unusual X-Mailer: {xm}")
        else:
            self.add_result('X-Mailer', 'INFO', 'No X-Mailer header')