import os
import pickle
from typing import Optional

class YouTubeUploader:
    """YouTube视频上传器"""
    
    def __init__(self, credentials_file: str = "credentials.json"):
        """
        初始化YouTube上传器
        
        参数:
            credentials_file: OAuth凭证文件路径
        """
        self.credentials_file = credentials_file
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """
        OAuth2认证
        """
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
            
            creds = None
            if os.path.exists("token.pickle"):
                with open("token.pickle", "rb") as token:
                    creds = pickle.load(token)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_file):
                        print(f"✗ 凭证文件不存在: {self.credentials_file}")
                        return
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                with open("token.pickle", "wb") as token:
                    pickle.dump(creds, token)
            
            self.youtube = build("youtube", "v3", credentials=creds)
            print("✓ YouTube认证成功")
        
        except Exception as e:
            print(f"✗ YouTube认证失败: {str(e)}")
    
    def upload_video(
        self,
        title: str,
        description: str,
        video_path: str,
        tags: list = None,
        category_id: str = "24",
        visibility: str = "private"
    ) -> Optional[str]:
        """
        上传视频到YouTube
        
        参数:
            title: 视频标题
            description: 描述
            video_path: 视频文件路径
            tags: 标签列表
            category_id: 视频分类ID
            visibility: 隐私设置 (private/unlisted/public)
        
        返回:
            视频ID，失败返回None
        """
        if not self.youtube:
            print("✗ YouTube客户端未初始化")
            return None
        
        if not os.path.exists(video_path):
            print(f"✗ 视频文件不存在: {video_path}")
            return None
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            tags = tags or []
            
            request_body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": category_id,
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": visibility,
                    "selfDeclaredMadeForKids": False
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=request_body,
                media_body=media
            )
            
            print(f"正在上传: {title}")
            response = request.execute()
            video_id = response['id']
            
            print(f"✓ YouTube上传成功")
            print(f"  Video ID: {video_id}")
            print(f"  URL: https://www.youtube.com/watch?v={video_id}")
            
            return video_id
        
        except Exception as e:
            print(f"✗ YouTube上传失败: {str(e)}")
            return None
