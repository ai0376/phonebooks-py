# API for PhoneBooks

请求方式： HTTP POST
数据交换格式： JSon

## 注册(register)

```
{
    "op":1001,
    "phone":"13000000001",
    "email":"13000000001@163.com",
    "name":"zhangsan",
    "password":"md5(123456)",
    "intime":"20170501000000"
}
```

## 登录
```
{
    "op":1003,
    "phone":"13000000001",
    "password":"123456"
}
```
## 人员添加
```
{
    "op":1005,
    "rid":"001",
    "users":[
        {
            "name":"a",
            "phones":[
                {
                    "phone":"13503768823"
                }
            ],
            "mails":[
                {
                    "mail":"1@qq.com"
                }
            ]
        }
    ]
}
```
## 人员删除
```
{
    "op":1007,
    "users":[
        {
            "uid":"001"
        }
    ]
}
```

## 人员修改
```
{
    "op":1006,
    "uid":"9d7d8361-32fe-11e7-9f7f-645a0434f13b",
    "user":{
        "name":"a",
        "phones":[
            {
                "pid":"9e696a00-32fe-11e7-b72b-645a0434f13b",
                "phone":"13503768823"
            },
            {
                "phone":"13503768800"
            }
        ],
        "mails":[
            {
                "mid":"9f193200-32fe-11e7-8d81-645a0434f13b",
                "mail":"1@qq.com"
            },
            {
                "mail":"88@qq.com"
            }
        ]
    }
}
```

## 人员查询
```
{
    "op":1009,
    "rid":"10b358cf-3185-11e7-9fd3-3010b3c7bffa"
}
```


#  Dependent Packages

environment  **python 2.7.x**

`pip install web.py`

`pip install MySQL-python`

`pip install python-memcached`


 


