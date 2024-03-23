# 项目说明/Project description
<a href="https://wakatime.com/badge/user/b415f305-24f8-432e-8d25-a46c15eba566/project/018dc496-d190-42b6-b317-2d03640e2315"><img src="https://wakatime.com/badge/user/b415f305-24f8-432e-8d25-a46c15eba566/project/018dc496-d190-42b6-b317-2d03640e2315.svg" alt="waketime" style="height:20px"></a>  <img src="https://badgen.net/static/license/Apache2/blue" style="height:20px">
### 语言/Language
#### [中文使用说明](#中文使用说明)
#### [English Guide](#english-user-guide)

## 中文使用说明
### 项目说明
本项目是使用机器学习模型对颜色视觉图像进行直线拟合。
本项目基于`FastAPI`和`Vue3.0`开发，源码中已包含前后端。
> *<u>注释：FastAPI后端文件位于OnlineV1文件夹中</u>*
### 项目依赖
本项目依赖环境
> ##### 前端依赖
> `Node.js 18.0+` 、 `Vue@CIL 5.0～`

> ##### 后端依赖
> `Python 3.8+` 、 `FastAPI 0.109.0+`
### 本地部署调试指南
> 配置项目之前确保安装有[Node.js 18.0+](https://nodejs.org/en)以及[Python 3.8+](https://www.python.org)并且配置完成系统环境

#### 前端调试/部署说明

安装Vue@CIL

```
npm install -g @vue/cli
# OR
yarn global add @vue/cli
```

`*在安装Vue@CIL之前请确保你已经安装了Node.js*`

安装运行组件库

`请务必进入项目根目录`

```
npm install
```

本地运行或实时编辑与测试

```
npm run serve
```

浏览器打开`localhost:8080`

`如不能正常运行，请检查报错信息，或本地8080端口是否被占用`

发布页面

```
npm run build
```

导出后的文件位于根目录dist文件夹中，您可以将其部署到`apache`，`nginx`或是其他web服务器中

#### 后端调试/部署说明

进入后端主目录

```
cd OnlineV1
```

确保您安装了`Python 3.8+`并且有自己的包管理工具
并且安装以下包

```
pip install fastapi uvicorn python-multipart opencv-python numpy pandas scikit-learn scipy websocket
```

运行和调试FastAPI

```
uvicorn server:app --reload
```

部署到服务器请参考[官方文档](https://fastapi.tiangolo.com/zh/deployment/)

### 开源许可说明

本项目根据Apache License 2.0（以下简称"许可"）授权。除非遵守许可，否则您不得使用此文件。

您可以在项目发行中或者[获取许可的副本](http://www.apache.org/licenses/LICENSE-2.0)。

除非适用法律要求或书面同意，根据许可分发的软件按"原样"分发，不附带任何明示或暗示的保证或条件。请参阅许可了解特定语言的权限和限制。

## English User Guide

### Project Description

This project involves fitting straight lines to color visual images using machine learning models. It is developed based on `FastAPI` and `Vue3.0`, with both front-end and back-end included in the source code.

> *<u>Note: The FastAPI backend files are located in the OnlineV1 folder</u>*

### Project Dependencies

This project relies on the following environment:

> ##### Frontend Dependencies
>
> `Node.js 18.0+` 、 `Vue@CIL 5.0～`

> ##### Backend Dependencies
>
> `Python 3.8+` 、 `FastAPI 0.109.0+`

### Local Deployment and Debugging Guide

Before configuring the project, ensure that you have installed [Node.js 18.0+](https://nodejs.org/en) and [Python 3.8+](https://www.python.org/) and have completed the system environment configuration.

#### Frontend Debugging/Deployment Instructions

Install Vue@CIL

```
npm install -g @vue/cli
# OR
yarn global add @vue/cli
```

*Make sure you have installed Node.js before installing Vue@CIL.*

Install and run component library

`Make sure you are in the project root directory.`

```
npm install
```

Run locally or edit and test in real-time

```
npm run serve
```

Open your browser and go to `localhost:8080`

`If it cannot run properly, check the error message or if port 8080 is occupied locally.`

Publish the page

```
arduinoCopy code
npm run build
```

The exported files are located in the root directory's dist folder, and you can deploy them to `apache`, `nginx`, or other web servers.

#### Backend Debugging/Deployment Instructions

Enter the backend main directory

```
bashCopy code
cd OnlineV1
```

Make sure you have installed `Python 3.8+` and have your package manager. Then install the following packages

```
Copy code
pip install fastapi uvicorn python-multipart opencv-python numpy pandas scikit-learn scipy websocket
```

Run and debug FastAPI

```
luaCopy code
uvicorn server:app --reload
```

For deployment to the server, please refer to the [official documentation.](https://fastapi.tiangolo.com/zh/deployment/)

### Open Source License Statement

This project is licensed under the Apache License 2.0 (hereinafter referred to as “License”). You may not use this file except in compliance with the License.

You may obtain a copy of the License in the project distribution or at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. Please see the License for the specific language governing permissions and limitations under the License.
