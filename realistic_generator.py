import random
import datetime
import hashlib

class RealisticHeaderGenerator:
    """Generador de cabeceras realistas con perfiles detallados."""

    def __init__(self):
        self.profiles = {
            'gmail_web': {
                'name': 'Gmail Web',
                'servers': ['mail-sor-f41.google.com', 'mail-ed1-f53.google.com'],
                'ips': ['209.85.220.41', '2a00:1450:4864:20::42'],
                'mx': ['mx.google.com', 'aspmx.l.google.com'],
                'x_mailer': None,
                'extra_headers': [
                    ('X-Gm-Message-State', 'AOAM530zrVw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8='),
                    ('X-Google-Smtp-Source', 'ABdhPJxKjYw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8=')
                ],
                'dkim_domain': 'gmail.com',
                'envelope_domain': 'gmail.com'
            },
            'gmail_android': {
                'name': 'Gmail App Android',
                'servers': ['mail-sor-f41.google.com', 'mail-ed1-f53.google.com'],
                'ips': ['209.85.220.41', '2a00:1450:4864:20::42'],
                'mx': ['mx.google.com', 'aspmx.l.google.com'],
                'x_mailer': 'Gmail App Android 2022.08.28',
                'extra_headers': [
                    ('X-Gm-Message-State', 'AOAM530zrVw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8='),
                    ('X-Google-Smtp-Source', 'ABdhPJxKjYw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8=')
                ],
                'dkim_domain': 'gmail.com',
                'envelope_domain': 'gmail.com'
            },
            'gmail_ios': {
                'name': 'Gmail App iOS',
                'servers': ['mail-sor-f41.google.com', 'mail-ed1-f53.google.com'],
                'ips': ['209.85.220.41', '2a00:1450:4864:20::42'],
                'mx': ['mx.google.com', 'aspmx.l.google.com'],
                'x_mailer': 'Gmail App iOS 2022.08.28',
                'extra_headers': [
                    ('X-Gm-Message-State', 'AOAM530zrVw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8='),
                    ('X-Google-Smtp-Source', 'ABdhPJxKjYw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8=')
                ],
                'dkim_domain': 'gmail.com',
                'envelope_domain': 'gmail.com'
            },
            'outlook_desktop': {
                'name': 'Outlook Desktop',
                'servers': ['BN7PR01MB6125.prod.exchangelabs.com', 'BN8PR01MB6126.prod.exchangelabs.com'],
                'ips': ['2603:10a6:208:380::18', '40.92.17.66'],
                'mx': ['mail.protection.outlook.com'],
                'x_mailer': 'Microsoft Outlook 16.0.14326.20450',
                'extra_headers': [
                    ('X-MS-Exchange-Organization-AuthAs', 'Internal'),
                    ('X-MS-Has-Attach', 'no')
                ],
                'dkim_domain': None,
                'envelope_domain': None
            },
            'outlook_web': {
                'name': 'Outlook Web',
                'servers': ['BN7PR01MB6125.prod.exchangelabs.com', 'BN8PR01MB6126.prod.exchangelabs.com'],
                'ips': ['2603:10a6:208:380::18', '40.92.17.66'],
                'mx': ['mail.protection.outlook.com'],
                'x_mailer': None,
                'extra_headers': [
                    ('X-MS-Exchange-Organization-AuthAs', 'Internal'),
                    ('X-MS-Has-Attach', 'no')
                ],
                'dkim_domain': None,
                'envelope_domain': None
            },
            'outlook_mobile': {
                'name': 'Outlook Mobile',
                'servers': ['BN7PR01MB6125.prod.exchangelabs.com', 'BN8PR01MB6126.prod.exchangelabs.com'],
                'ips': ['2603:10a6:208:380::18', '40.92.17.66'],
                'mx': ['mail.protection.outlook.com'],
                'x_mailer': 'Outlook for iOS 4.2232.0',
                'extra_headers': [
                    ('X-MS-Exchange-Organization-AuthAs', 'Internal'),
                    ('X-MS-Has-Attach', 'no')
                ],
                'dkim_domain': None,
                'envelope_domain': None
            },
            'iphone_icloud': {
                'name': 'iPhone with iCloud',
                'servers': ['a17-123.apple.com', 'a18-45.apple.com'],
                'ips': ['17.57.144.123', '17.142.160.45'],
                'mx': ['mx1.icloud.com', 'mx2.icloud.com'],
                'x_mailer': 'iPhone Mail 15.1',
                'extra_headers': [
                    ('X-Proofpoint-Virus-Version', 'vendor=fsecure engine=2.50.10434:6.0.425,18.0.794')
                ],
                'dkim_domain': 'icloud.com',
                'envelope_domain': 'icloud.com'
            },
            'iphone_gmail': {
                'name': 'iPhone with Gmail',
                'servers': ['mail-sor-f41.google.com', 'mail-ed1-f53.google.com'],
                'ips': ['209.85.220.41', '2a00:1450:4864:20::42'],
                'mx': ['mx.google.com', 'aspmx.l.google.com'],
                'x_mailer': 'iPhone Mail 15.1 (with Gmail)',
                'extra_headers': [
                    ('X-Gm-Message-State', 'AOAM530zrVw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8='),
                    ('X-Google-Smtp-Source', 'ABdhPJxKjYw4G0WYXh5v9kE5KqYj8h5J7kYz2q1vF8=')
                ],
                'dkim_domain': 'gmail.com',
                'envelope_domain': 'gmail.com'
            },
            'exchange_onprem': {
                'name': 'Exchange On-Premise',
                'servers': ['mail.empresa.local', 'exch01.empresa.com'],
                'ips': ['10.10.1.25', '192.168.1.50'],
                'mx': ['mx.empresa.com'],
                'x_mailer': 'Microsoft Exchange Server 2019',
                'extra_headers': [
                    ('X-MS-Exchange-Organization-SCL', '0'),
                    ('X-MS-Exchange-Organization-PCL', '0')
                ],
                'dkim_domain': None,
                'envelope_domain': None
            },
            'zimbra': {
                'name': 'Zimbra',
                'servers': ['mail.zimbra.com', 'zm-host1.zimbra.com'],
                'ips': ['8.8.8.8', '1.1.1.1'],
                'mx': ['mx.zimbra.com'],
                'x_mailer': 'Zimbra 8.8.15',
                'extra_headers': [
                    ('X-Zimbra-SPF', 'pass'),
                    ('X-Zimbra-DKIM', 'pass')
                ],
                'dkim_domain': None,
                'envelope_domain': None
            }
        }
        self.all_servers = []
        for p in self.profiles.values():
            self.all_servers.extend(p['servers'])

    def get_profile_names(self):
        return [(key, p['name']) for key, p in self.profiles.items()]

    def generate_received_chain(self, profile_key, length=2, with_private=False):
        profile = self.profiles[profile_key]
        chain = []
        dest_server = random.choice(profile['mx'])
        for i in range(length):
            if i == 0:
                from_server = random.choice(profile['servers'])
                from_ip = random.choice(profile['ips'])
                to_server = dest_server
            else:
                from_server = random.choice(self.all_servers)
                if with_private and random.random() < 0.3:
                    from_ip = f"192.168.{random.randint(1,254)}.{random.randint(1,254)}"
                else:
                    from_ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                to_server = random.choice(self.all_servers)
            timestamp = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(5, 60) * (i+1))
            timestamp_str = timestamp.strftime('%a, %d %b %Y %H:%M:%S')
            tz = random.choice(['-0500', '-0600', '-0700', '-0800', '+0000', '+0100', '+0200'])
            tx_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=12))
            received = f"from {from_server} ({from_server} [{from_ip}]) by {to_server} with ESMTPS id {tx_id}; {timestamp_str} {tz}"
            chain.append(received)
        return chain

    def generate_authentication_results(self, from_domain, envelope_domain, dkim_domain=None, error_mode='none'):
        if error_mode == 'spf_fail':
            spf_result = 'fail'
        elif error_mode == 'spf_neutral':
            spf_result = 'neutral'
        else:
            spf_result = 'pass' if envelope_domain == from_domain else 'softfail'

        if error_mode == 'dkim_fail':
            dkim_result = 'fail'
        elif error_mode == 'dkim_neutral':
            dkim_result = 'neutral'
        else:
            dkim_result = 'pass' if dkim_domain == from_domain else 'fail' if dkim_domain else 'none'

        if error_mode == 'dmarc_fail':
            dmarc_result = 'fail'
        else:
            dmarc_result = 'pass' if (spf_result == 'pass' or dkim_result == 'pass') else 'fail'

        auth = f"mx.google.com;\n       spf={spf_result} smtp.mailfrom=@{envelope_domain};\n"
        if dkim_domain:
            auth += f"       dkim={dkim_result} header.i=@{dkim_domain};\n"
        auth += f"       dmarc={dmarc_result} (p=QUARANTINE sp=QUARANTINE dis=NONE) header.from={from_domain}"
        return auth

    def generate_message_id(self, domain):
        timestamp = int(datetime.datetime.now().timestamp())
        random_part = hashlib.md5(str(random.random()).encode()).hexdigest()[:12]
        if 'gmail.com' in domain:
            return f"<{timestamp}.{random_part}@mail.gmail.com>"
        elif 'outlook.com' in domain or 'microsoft.com' in domain:
            return f"<{timestamp}.{random_part}@{domain}>"
        else:
            return f"<{timestamp}.{random_part}@{domain}>"

    def generate_dkim_signature(self, domain, selector='20210112'):
        bh = hashlib.sha256(str(random.random()).encode()).hexdigest()[:16]
        b = hashlib.sha256(str(random.random()).encode()).hexdigest()[:32]
        return (f"v=1; a=rsa-sha256; c=relaxed/relaxed; d={domain}; s={selector}; "
                f"t={int(datetime.datetime.now().timestamp())}; h=from:to:subject:date:message-id; "
                f"bh={bh}; b={b}")