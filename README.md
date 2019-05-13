# Douyin-videos-download
配合Fiddler抓取手机app抖音的视频地址，达到下载的目的



在Fiddler的脚本加入以下代码：
if(oSession.fullUrl.Contains('ixigua'))
        {
            var filepath = "复制py脚本上面的地址"
            var video_url = oSession.fullUrl + "\r\n"
            var filename = filepath + ""+(new Date()).valueOf() + Math.round(Math.random()*1000 +1000) +".txt"
            var sw = System.IO.File.CreateText(filename); 
            sw.Write(video_url);
            sw.Close();  
            sw.Dispose();
        }
 

点击py脚本开始监听，下载手机上看的抖音视频
