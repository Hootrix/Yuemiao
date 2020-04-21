# Yuemiao
约苗HPV 抢苗时间预览

## 目的

查看指定城市中哪些社区可预约，用做准备未来手动预约抢苗。

自动抢苗操作不能实现，毕竟有各种数学运算的验证码。


## 使用

1. 微信客户端登录：https://wx.healthych.com/index.html#/home?fa=wx&t= 

2. 使用 Fiddler 或者 Charles 拿到登录之后`wx.healthych.com`域名下的任一请求的cookies 请求头`tk`

如 `fvfe3c1o9O81fdc3b7809397a42fa7ba0_948c572780f01baa99faef0a7a05f213`

3. 修改此处[134L处代码](https://github.com/Hootrix/Yuemiao/blob/master/Yuemiao.py#L134)

