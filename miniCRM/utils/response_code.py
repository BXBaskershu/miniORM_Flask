class RET:
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    SALESMANERR = "4104"
    CUSTOMERERR = "4105"
    PWDERR = "4106"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"


error_map = {
    RET.OK: "ok",
    RET.DBERR: "数据库查询错误",
    RET.NODATA: "无数据",
    RET.DATAEXIST: "数据已存在",
    RET.DATAERR: "数据错误",
    RET.SESSIONERR: "销售人员未登录",
    RET.LOGINERR: "销售登录失败",
    RET.PARAMERR: "参数错误",
    RET.SALESMANERR: "销售人员不存在",
    RET.CUSTOMERERR: "客户身份错误",
    RET.PWDERR: "密码错误",
    RET.REQERR: "非法请求或请求次数受限",
    RET.IPERR: "IP受限",
    RET.THIRDERR: "第三方系统错误",
    RET.IOERR: "文件读写错误",
    RET.SERVERERR: "内部错误",
    RET.UNKOWNERR: "未知错误",
}
