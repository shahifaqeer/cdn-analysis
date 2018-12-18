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


def main():
    """Test function"""

    import json
    from CDNdomains import cdn_domains, cdn_names
    all_cdn_names = list(set(cdn_names + list(cdn_domains.values())))

    site_to_IP = json.load(open('output/site_to_IP.json', 'r'))
    for site, IP in site_to_IP.items():

        whois1 = loadwhoisIP(site)
        Org1 = searchOrg(whois1)
        Email = searchEmail(whois1)

        whois2 = loadwhoisIP(site)
        Org2 = searchOrg(whois2)

        print("\twhois " + site + " | ", end="")
        print(Org1, end=" | ")
        print(Org2)

        i = 0       # count and print all matches while testing
        for org in list( set(Org1+Org2) ):
            for cdn in all_cdn_names:
                if (org.lower() in cdn.lower()) or (cdn.lower() in org.lower()):
                    print(site + "cdn match "+str(i)+" : " + cdn)
                    i += 1
        print()
    return


if __name__ == '__main__':

    main()
