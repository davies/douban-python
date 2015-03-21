## Examples of douban-python ##

1，请先申请[API\_KEY](http://www.douban.com/service/apikey/)，得到API\_KEY和私钥。

2，如下命令完成了API认证过程：
```
client = douban.service.DoubanService(server=SERVER, api_key=API_KEY,secret=SECRET)
client.ProgrammaticLogin(token_key=TOKEN_KEY,token_secret=TOKEN_SECRET)
```
运行上述代码时，输出如下提示信息：
```
please paste the url in your webbrowser, complete the authorization then come back:
http://www.douban.com/service/auth/authorize?oauth_token=5d6f7b964ef6f60c184e72c2ece4e224

```
将上述url连接拷贝到浏览器，进入到douban api认证授权页面，点击同意，即可完成对本次api访问的授权。

3，正常的api操作。下面例举了几个简单的应用：
```
people = client.GetPeople('/people/1000001')
assert people.uid.text == 'ahbei'
assert people.title.text == "阿北"
assert people.location.text == "北京"

feed = client.SearchPeople("阿北")
assert any( e.title.text == "阿北" for e in feed.entry)

people = client.GetAuthorizedUID('/people/@me')
assert people.uid.text == '2463802'
```

更多示例，请参考test\_service.py