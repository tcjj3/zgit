# zgit

zgit是一个`git`命令的wrapper，使用github镜像，提高 `git clone https://github.com/... `的速度。
同时，添加了自动执行 `git remote set-url ...` 的便捷操作。


## 依赖
- `python`：python3.5+
- `git`：使用`git`命令。如果找不到`git`命令则通过环境变量`GIT`查找`git`可执行文件


## 安装
只需下载到本地，放到可使用的目录即可。
建议把所在目录加入`PATH`环境变量。

Linux：
```shell
sudo wget https://raw.githubusercontent.com/yantaozhao/zgit/main/zgit.py -O /usr/local/bin/zgit && sudo chmod +x /usr/local/bin/zgit
```


## 使用方法：
用法同`git`.

> `zgit`是一个python脚本，有执行权限时可以直接运行`zgit clone ...`，也可以使用python解释器执行`python zgit clone ...`。

例如：
```shell
zgit clone https://github.com/tensorflow/tensorflow.git
```

使用 `zgit -h` 查看详细用法。


## 参考：

https://github.com/ant-design/ant-design-pro/issues/4823

https://gitee.com/killf/cgit
