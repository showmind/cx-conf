import requests
import json

from gen_rules_config import gen_rules_conf
from gen_simple_config import gen_simple_conf

url = "https://api.hostmonit.com/get_optimization_ip"
headers = {
    "authority": "api.hostmonit.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json",
    "origin": "https://stock.hostmonit.com",
    "referer": "https://stock.hostmonit.com/",
    "sec-ch-ua": '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76"
}


vless_tpl = """vless://6386b476-d9b1-4ec8-953c-d682a22a01f7@{ip}:80?encryption=none&security=none&sni=hello.patvice.workers.dev&fp=randomized&type=ws&host=hello.patvice.workers.dev&path=%2F%3Fed%3D2048#{name}
"""

clash_tpl = """  - type: vless
    name: {name}
    server: {ip}
    port: 443
    uuid: 6386b476-d9b1-4ec8-953c-d682a22a01f7
    network: ws
    tls: true
    udp: false
    sni: cfhello.patvice.top
    client-fingerprint: chrome
    skip-cert-verify: flase
    ws-opts:
      path: "/?ed=2048"
      headers:
        host: cfhello.patvice.top
"""


def ips():
    data = json.dumps({"key": "iDetkOys"})

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("请求成功")
        json_data = response.json()
        if json_data["code"] == 200:
            print("获取成功")
            return json_data["info"]

    else:
        print("请求失败，状态码：", response.status_code)


if __name__ == '__main__':
    host_list = ips()

    vless_tplstr = ""
    clash_tplstr = ""
    names = []

    servers = []

    # prefer server

    servers.append({"ip": "162.159.134.216", "name": "HKG"})
    servers.append({"ip": "104.17.212.213", "name": "SJC"})

    for server in host_list:
        dic = {"ip": server['ip'], "name": 'Worker-' +
               server['line']+'-'+server['colo']+'-'+server['ip']}
        servers.append(dic)

    for server in servers:
        print(server)
        vless_tplstr += vless_tpl.format(**server)
        clash_tplstr += clash_tpl.format(**server)
        names.append(server['name'])

    with open('vless.txt', 'w') as f:
        f.write(vless_tplstr)

    with open('clash-proxies.yaml', 'w') as f:
        f.write(clash_tplstr)

    gen_rules_conf(clash_tplstr, names)
    print(clash_tplstr)
    gen_simple_conf(clash_tplstr, names)
