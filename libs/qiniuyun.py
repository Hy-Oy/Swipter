from qiniu import Auth, put_file

from common import config


def upload_qiniuyun(filename,filepath):
    #构建鉴权对象
    q = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)
    #上传后保存的文件名
    key = filename
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(config.QN_NAME, key, 3600)
    ret, info = put_file(token, key, filepath)
    return ret, info