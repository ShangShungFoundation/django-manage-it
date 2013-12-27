import xml.etree.ElementTree as ET
from dataforms.models import Answer


def scan(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    meta = dict(root.items())

    def map_h(h):
        el = list(h)  # h.getchildren()
        return el[1].items()[1][1], dict([[e.tag, e.attrib] for e in el])

    hosts = dict(map(map_h, root.iter("host")))
    #import ipdb; ipdb.set_trace()
    devices_ips = Answer.objects.filter(field=1).select_related("submissions")

    ips = dict(
        [[s.value, s.submission.slug] for s in devices_ips if s.value != ""])

    # asign slugs to devices
    hosts_up = {}
    hosts_alien = {}
    for host_ip in hosts:
        if hosts[host_ip]["status"]["state"] == "up":
            host = hosts[host_ip]
            if host_ip in ips:
                host["ip"] = host_ip
            #    host.slug = ips[host_ip]
                hosts_up[ips[host_ip]] = host
            else:
                hosts_alien[host_ip] = host

    #import ipdb; ipdb.set_trace()
    vars = dict(
        hosts_up=hosts_up,
        hosts_alien=hosts_alien,
        meta=meta,
        #trace=[r for r in root.iter("trace")],
    )
    return vars
