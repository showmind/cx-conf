import os

import yaml
from typing import Dict, Any


class ClashConfig:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.config.setdefault('proxies', [])
        self.config.setdefault('proxy-groups', [])

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value

    def to_yaml(self) -> str:
        return yaml.dump(self.config, allow_unicode=True)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "ClashConfig":
        config = yaml.safe_load(yaml_str)
        return cls(config)

    def add_proxy(self, proxy: dict):
        proxies = self.config['proxies']
        if not proxies:
            proxies = self.config['proxies'] = []
        proxy_groups = self.config['proxy-groups']

        if not proxy['name']:
            print("wrong proxy: ", proxy)
            return
        proxies.append(proxy)
        for pg in proxy_groups:
            if not pg['proxies']:
                pg['proxies'] = []
            pg['proxies'].append(proxy['name'])


# 示例

def gen_config_file(tpl, vless_list):
    config_yaml = ''

    with open(tpl, encoding='utf-8') as file:
        config_yaml = file.read()

    config = ClashConfig.from_yaml(config_yaml)
    print(config.config)  # 输出 "proxy1"

    warp_wg = {
        'type': 'wireguard',
        'name': 'cloudfare-warp+',
        "server": "188.114.98.35",
        "port": 8742,
        "ip": '172.16.0.2',
        "private-key": 'oOeEcGFgtmIEE3I1bS/DNZfKIgiG6C9WC6ZvRkPkwVE=',
        'public-key': 'bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo='
    }

    config.add_proxy(warp_wg)



    name_= os.path.basename(tpl).lstrip("tpl_")
    with open(name_, mode="w", encoding='utf-8') as file:
        file.write(config.to_yaml())
