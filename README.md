# Youtube 播放清單管理

## 創建自己的API

在操作這個專案之前，需要先驗證你的google帳號，最好是已經有頻道的youtube帳號
接下來，需要進行驗證以及申請，請進[Google Cloud Platform]([article-name.md](https://console.cloud.google.com))
你會看到這個畫面:
![](./picture/登入畫面.png)

接下來，在API和服務中，點入「憑證」，分別創建API金鑰跟OAuth 2.0 用戶端 ID
完成之後的結果如下所示:
![](./picture/創建.png)

最後，需要下載OAuth 2.0 用戶端的.json檔，點擊畫面最左邊的「下載OAuth用戶端」，**放進跟這個專案一樣的資料夾內**，名稱改成你喜歡的名稱。
==注意!!  在程式碼中記得修改檔案名稱!==

```py
client_secrets_file = "your_file_name.json" #remember to change name here !
```

大功告成，接下來是實作的部分

## Demo 流程

**開始使用youtube api**

https://developers.google.com/youtube/v3/getting-started

https://developers.google.com/youtube/registering_an_application