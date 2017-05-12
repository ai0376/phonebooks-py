# API for PhoneBooks

请求方式： HTTP POST
数据交换格式： JSon

## 注册(register)

request

```
{
    "op":1001,
    "phone":"13000000001",
    "email":"13000000001@163.com",
    "name":"zhangsan",
    "password":"123456"
}
```
respon

```
{
    "msg":"success",
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa",
    "ret":0
}
```

## 登录

request

```
{
    "op":1003,
    "phone":"13000000001",
    "password":"123456"
}
```

respon

```
{
    "msg":"success",
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa",
    "num":0,
    "token":{
        "access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE0OTQ0OTI2MTcsInVpZCI6IjcwYTI2ZWMwLTM2MjYtMTFlNy1iNmRhLTMwMTBiM2M3YmZmYSIsImV4cCI6MTQ5NDQ5MzgxN30.TcvSgm-gmZeJ7O6AJkyrHacAo8MtTcHHM_4U8NkOZWQ",
        "type":"JWT"
    },
    "ret":0
}
```
## 人员添加

header 中需要携带

`AUTHORIZATION: JWT access_token`

request

```
{
    "op":1005,
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa",
    "users":[
        {
            "name":"a",
            "phones":[
                {
                    "phone":"13503768800"
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

respon

```
{
    "msg":"success",
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa",
    "users":[
        {
            "phones":[
                {
                    "phone":"13503768800",
                    "pid":"69e5ecf0-3627-11e7-b53b-3010b3c7bffa",
                    "intime":"20170511165412",
                    "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa"
                }
            ],
            "mails":[
                {
                    "mail":"1@qq.com",
                    "intime":"20170511165412",
                    "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa",
                    "mid":"6a3174e1-3627-11e7-9816-3010b3c7bffa"
                }
            ],
            "intime":"20170511165412",
            "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa",
            "name":"a"
        }
    ],
    "ret":0
}
```
## 人员删除

header 中需要携带

`AUTHORIZATION: JWT access_token`

request

```
{
    "op":1007,
    "users":[
        {
            "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa"
        }
    ]
}
```

respon

```
{
    "msg":"success",
    "ret":0
}
```

## 人员修改

header 中需要携带

`AUTHORIZATION: JWT access_token`

request

```
{
    "op":1006,
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "user":{
        "name":"刘可",
        "phones":[
            {
                "pid":"fd1fe5c0-3627-11e7-8972-3010b3c7bffa",
                "phone":"135012345678"
            },
            {
                "phone":"13503768800"
            }
        ],
        "mails":[
            {
                "mid":"fd6998f0-3627-11e7-8588-3010b3c7bffa",
                "mail":"5678@qq.com"
            },
            {
                "mail":"88@qq.com"
            }
        ]
    }
}
```
respon
```
{
    "msg":"success",
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "ret":0,
    "user":{
        "phones":[
            {
                "phone":"135012345678",
                "pid":"fd1fe5c0-3627-11e7-8972-3010b3c7bffa",
                "intime":"20170511170304"
            },
            {
                "phone":"13503768800",
                "pid":"a644fbde-3628-11e7-b491-3010b3c7bffa",
                "intime":"20170511170307"
            }
        ],
        "mails":[
            {
                "mail":"5678@qq.com",
                "intime":"20170511170307",
                "mid":"fd6998f0-3627-11e7-8588-3010b3c7bffa"
            },
            {
                "mail":"88@qq.com",
                "intime":"20170511170308",
                "mid":"a6c3efde-3628-11e7-ba0f-3010b3c7bffa"
            }
        ],
        "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
        "name":"刘可"
    }
}
```

## 个人手机号管理

header 中需要携带

`AUTHORIZATION: JWT access_token`

```
action = 0 is add 

{
    "op":10061,
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "action":0,
    "phone_info":{
        "phone":"13000001234"
    }
}

action = 1 is delete

{
    "op":10061,
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "action":1,
    "phone_info":{
        "pid":"69e5ecf0-3627-11e7-b53b-3010b3c7bffa"
    }
}
```

## 个人邮箱管理

header 中需要携带

`AUTHORIZATION: JWT access_token`

```
action = 0 is add 

{
    "op":10062,
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "action":0,
    "mail_info":{
        "mail":"13000001234@qq.com"
    }
}

action = 1 is delete

{
    "op":10062,
    "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
    "action":1,
    "mail_info":{
        "mid":"69e5ecf0-3627-11e7-b53b-3010b3c7bffa"
    }
}

## 获取所有人
header 中需要携带

`AUTHORIZATION: JWT access_token`

request

```
{
    "op":1009,
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa"
}
```
respon

```
{
    "msg":"success",
    "rid":"70a26ec0-3626-11e7-b6da-3010b3c7bffa",
    "users":[
        {
            "phones":[
                {
                    "intime":"20170511165412",
                    "pid":"69e5ecf0-3627-11e7-b53b-3010b3c7bffa",
                    "phone":"13503768800"
                }
            ],
            "mails":[
                {
                    "mail":"1@qq.com",
                    "intime":"20170511165412",
                    "mid":"6a3174e1-3627-11e7-9816-3010b3c7bffa"
                }
            ],
            "intime":"20170511165412",
            "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa",
            "name":"a"
        },
        {
            "phones":[
                {
                    "intime":"20170511170307",
                    "pid":"a644fbde-3628-11e7-b491-3010b3c7bffa",
                    "phone":"13503768800"
                },
                {
                    "intime":"20170511170304",
                    "pid":"fd1fe5c0-3627-11e7-8972-3010b3c7bffa",
                    "phone":"135012345678"
                }
            ],
            "mails":[
                {
                    "mail":"88@qq.com",
                    "intime":"20170511170308",
                    "mid":"a6c3efde-3628-11e7-ba0f-3010b3c7bffa"
                },
                {
                    "mail":"5678@qq.com",
                    "intime":"20170511170307",
                    "mid":"fd6998f0-3627-11e7-8588-3010b3c7bffa"
                }
            ],
            "intime":"20170511165820",
            "uid":"fb0f7c4f-3627-11e7-b806-3010b3c7bffa",
            "name":"刘可"
        }
    ],
    "ret":0
}
```

## 人员查询

`AUTHORIZATION: JWT access_token`

request

```
{
    "op":1010,
    "users":[
        {
            "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa"
        }
    ]
}
```
respon

```
{
    "msg":"success",
    "users":[
        {
            "phones":[
                {
                    "intime":"20170511165412",
                    "pid":"69e5ecf0-3627-11e7-b53b-3010b3c7bffa",
                    "phone":"13503768800"
                }
            ],
            "mails":[
                {
                    "mail":"1@qq.com",
                    "intime":"20170511165412",
                    "mid":"6a3174e1-3627-11e7-9816-3010b3c7bffa"
                }
            ],
            "intime":"20170511165412",
            "uid":"6796a5c0-3627-11e7-95ab-3010b3c7bffa",
            "name":"a"
        }
    ],
    "ret":0
}
```

#  Dependent Packages

environment  **python 2.7.x**

`pip install web.py`

`pip install MySQL-python`


 


