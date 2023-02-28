from . import crypt
from . import resources
from xml.etree import ElementTree
from enum import Enum
import hashlib, json, requests

class Roles(Enum):
    NONE = 0
    MEMBER = 2
    PATREON = 4
    SA = 8
    DIGGER = 16
    SPACEMAN = 16
    GRANTOR = 32
    MEGACARDUSER = 64
    MODERATOR = 131072
    ADMINISTRATOR = 262144
    CHIEF = 524288
    HIDDEN = 1048576

class Client:
    def __init__(self, login, password):
        self._session = requests.Session()
        self._login(login, password)
        user_data = self._load_server_xml("ServerAction", "<root user=\"\" platform=\"17\" />")
        user = user_data.find("user")
        self.user_name = user_data.find("user_name").get("Value")
        self.user_id = int(user.get("UserId"))
        self.user_role = Roles(int(user.get("RoleFlags")))
    
    def _login(self, login, password):
        response = self._session.post("https://www.shararam.ru/api/user/login", data=json.dumps({"login": login, "password": hashlib.md5(password.encode("utf8")).hexdigest()}))
        result = response.json()
        if result["code"] != 0:
            raise ValueError(response.json()["error"])
    
    def _load_server_xml(self, path, data):
        response = self._session.post("https://www.shararam.ru/async/" + path, data=data)
        xml = ElementTree.fromstring(response.text)
        return ElementTree.fromstring(crypt.decrypt(xml.find(".").text))
    
    def get_servers(self):
        user_data = self._load_server_xml("ServerAction", "<root user=\"\" platform=\"17\" />")
        servers = user_data.find("servers")
        result = []
        for item in servers.findall("item"):
            result.append({
                "id": int(item.get("Id")),
                "name": resources.tr[int(item.get("TRId"))],
                "url": item.get("Url"),
                "load": int(item.get("Load")),
                "friends_count": int(item.get("FriendsCount")),
                "clubs_count": int(item.get("ClubsCount"))
            })
        return result
