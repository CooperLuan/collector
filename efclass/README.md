# EF Class Collector

这是一个 EF 线上课程的学习资料收集脚本, 目的是将学习过程中的例句/文章等单独保存，方便复习用

## 开发进度

- [ ] dotjs 部分
- [ ] dump 部分

## 使用

- `./deploy_to_dotjs.sh` 部署到 dotjs 目录
- 确保有可用的 `MongoDB Service`
- `./build.sh` 安装 python 环境
- `bin/python serve.py` 启动数据接收服务端
- 打开 [EF 线上课程](http://ec.ef.com.cn) 学习
- `bin/python dump.py`
