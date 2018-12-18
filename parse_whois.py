# search orgs for both whois IP and whois site
# search email only for whois IP

import os


def loadwhoisIP(site):
    file = 'output/whoisIP/'+site
    if os.path.exists(file):
        f = open(file, 'r')
        whoisIP = f.read()
        f.close()
        return whoisIP
    else:
        print("Please perform whois for site %s" %site)
        return None


def loadwhoissite(site):
    file = 'output/whoissite/'+site
    if os.path.exists(file):
        f = open(file, 'r')
        whoissite = f.read()
        f.close()
        return whoissite
    else:
        print("Please perform whois for site %s" %site)
        return None


def searchOrg(whoisdata):
    """ returns list of organization names """
    Org = []
    OrgKeywords = ['organisation:', 'org:', 'organization:', 'org-name:', 'orgname:']
    exclude_orgs = [e.lower() for e in ['AFRINIC', 'APNIC', 'ARIN', 'LACNIC', 'IANA',
                                        'Asia Pacific Network Information Centre', 'Administered by RIPE NCC',
                                        'RIPE NCC',
                                        'Registration Association', 'VeriSign Global Registry Services']]
    if whoisdata is not None:
        for line in whoisdata.split('\n'):
            lower_line = line.lower()

            for keyword in OrgKeywords:
                if keyword in lower_line:
                    if not any([excl_org in lower_line for excl_org in exclude_orgs]):
                        org = line.split(':')[1].strip()
                        if not (org in Org) and org != "":
                            Org.append(org)
    return Org


def searchEmail(whoisdata):
    Email = []
    EmailKeywords = ['@', 'email:', 'mailbox:', 'e-mail:']
    # exclude_emails = [e.lower() for e in ['verisign-grs.com', 'verisigninc.com', 'Registrar'] ]

    if whoisdata is not None:
        for line in whoisdata.split('\n'):
            lower_line = line.lower()

            for keyword in EmailKeywords:
                if keyword in lower_line:
                    email = line.split('@')[1].strip()
                    if not email in Email:
                        Email.append(email)

    return Email
