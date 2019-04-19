#Enter valid code while calling API.
#Keep cron time minimum 1 minute
date >> ~/virtual_env/catchpace-cafe-crawlers/jdscrapper/proxyrefreshtime.txt
wget "http://justapi.info/api/proxylist.php?type=s&anon=4&out=plain&code=691785319847986" -O freeproxylist.txt

