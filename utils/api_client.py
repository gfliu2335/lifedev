import requests
from config.settings import TIMEOUT, get_proxy

class APIClient:
    """统一的API客户端"""
    
    def __init__(self):
        self.timeout = TIMEOUT
        self.proxy = get_proxy()
        self.session = requests.Session()
        
        if self.proxy:
            self.session.proxies = {'http': self.proxy, 'https': self.proxy}
    
    def get(self, url: str, **kwargs) -> dict:
        """
        GET请求
        
        参数:
            url: 请求URL
            **kwargs: 其他参数
        
        返回:
            响应JSON
        """
        try:
            kwargs['timeout'] = kwargs.get('timeout', self.timeout)
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"✗ GET请求失败 {url}: {str(e)}")
            return {}
    
    def post(self, url: str, **kwargs) -> dict:
        """
        POST请求
        
        参数:
            url: 请求URL
            **kwargs: 其他参数
        
        返回:
            响应JSON
        """
        try:
            kwargs['timeout'] = kwargs.get('timeout', self.timeout)
            response = self.session.post(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"✗ POST请求失败 {url}: {str(e)}")
            return {}
