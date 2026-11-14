# 星衡能源 · 冷却代理模型因子敏感度

在明确物理范围的受控多项式代理上运行Morris与Sobol试验，把因子影响、采样预算、轨迹和复核依据放在同一份底稿中。

## 业务场景

星衡能源节能研究组是13人的模拟研究团队，负责比较冷却回路的候选试验方向。过去分析师在电子表格里逐个改变量，再用单因素扫表讨论改造方案：两两交互容易漏查，某一位置的斜率常被当成全局影响，采样量与模型版本也容易在汇报中丢失。

上游是 `XH-C06_202611.json` 的受控模拟系数与已声明的物理范围；本系统替代采样、代理函数评估、敏感度汇总和复核整理；下游是安排下一轮离线试验的研究主管。它不连接工业控制设备，不连接电表，也不将代理输出当作真实节能收益。

|角色|页面及权限|典型动作|
|---|---|---|
|analyst 分析师|查看六页；创建模型、因子空间、研究、运行及复核|检查交互项，提交因子试验|
|admin 研究主管|分析师权限；批准复核、生成快照、查看审计|签署假设与有限采样口径|
|viewer 研究助理|只读六页，下载批准的CSV|复用锁定底稿，不修改模型|

### 一天的试验记录

1. 09:00 分析师打开「XH-C06 冷却电耗模拟代理」，核对截距240 kWh、6个因子及3个交互项。
2. 09:05 核对冷却水流量18–30 m³/h、入口水温25–33°C、热负荷比0.45–0.95、风机频率30–50 Hz、逼近温差3–8°C、泵效率65–85%。这些是模拟范围，因子独立均匀。
3. 09:10 建立「XH-C06 归一因子敏感度底稿」：Morris r=24、p=6；Sobol m=12、基础n=4096；seed=20261112。
4. 09:15 执行后台试验；Morris实际168次评估，Sobol实际32768次评估，不把基础n误写成总评估数。
5. 09:20 比较μ*×σ与S1/ST，注意泵效率的负μ与正μ*；默认热负荷比ST约0.6196，不能解释成可实现61.96%的节能。
6. 09:25 点选load，核对24个EE和样本sigma分母23，切换网格轨迹检查下降步骤仍除以实际负步长。
7. 09:30 分析师提交说明；主管核对模型、范围、采样与假设后批准。
8. 09:40 助理下载6因子CSV，携带输入SHA256、评估数、网格、seed与限制说明归档。

## 六个业务聚合与页面

|聚合|职责|页面|
|---|---|---|
|ResponseModel|截距、因子线性/二次系数、两两交互项|响应模型|
|FactorSpace|对应模型的完整物理范围与分布假设|因子空间|
|SensitivityStudy|模型/范围绑定、r/p/m/seed锁定|采样研究|
|SensitivityRun|排队状态、完整输入与结果、EE轨迹和全局指数|运行底稿|
|FactorReview|研究说明与主管批准状态|试验归档|
|Report|批准后不可变快照与CSV|试验归档|

「因子总览」汇集真实基线结果；另有登录与管理员审计页。总览/运行共用Morris散点图、Sobol条形图和采样预算组件；模型系数在模型页与锁定运行中共用展示。

## 模型与输入限制

响应为 `intercept + Σc_i*x_i + Σq_i*x_i² + Σc_ij*x_i*x_j`，物理坐标x使用各因子声明单位，输出固定为模拟kWh。公式由Python显式加权计算，不使用eval，不接收任意表达式。2–6个因子；系数有限，绝对值≤1e6，截距绝对值≤1e12；因子ID唯一、ASCII字母起始，最长32字符。

模型CSV列为 `factor_id,name,unit,linear,quadratic`；交互CSV列为 `left,right,coefficient`。未知因子、自交互、重复因子、重复交互（包括反向重复）均拒绝；二次项通过quadratic单独声明。没有交互时仅保留交互CSV表头。

范围CSV列为 `factor_id,low,high`；必须完整覆盖对应模型且不重复，端点有限、绝对值≤10000，low<high。不自动推断单位、不执行单位转换。归一映射是 `x=low+u*(high-low)`，u∈[0,1]。所有因子被假设为独立均匀分布；相关输入需要别的方法，不能直接把本结果推广过去。

## 两个Python算法

### Morris网格轨迹

接口：`services.morris.morris(model,ranges,trajectories=24,levels=6,seed=20261112)`。

p为2–20的偶数；r为2–128。网格u为 `j/(p-1)`，`delta=p/[2*(p-1)]`。每条轨迹独立生成随机方向与因子顺序，选择保证正/负步均不越界的起点，每个因子恰改变一次。响应在物理范围映射后评估。基本效应为 `(f(next)-f(previous))/(u_next_i-u_previous_i)`，分母使用实际有符号归一步长；下降方向不把正线性效应反转成负数。

μ是r个EE均值，μ*是绝对值均值，σ是样本标准差ddof=1，分母r−1。单位是kWh/归一因子单位，因此已包含物理范围宽度。μ*用于影响大小筛查，σ反映非线性/交互造成的效应离散，不能由σ独立区分两者；σ也不是均值标准误或置信区间。实际模型评估数为r(d+1)，重复点仍按实际调用计数。

### Sobol / Saltelli一阶与Jansen总效应

接口：`services.sobol.sobol(model,ranges,power=12,seed=20261112)`。

基础n=2^m，m为2–16。使用 `scipy.stats.qmc.Sobol(2*d,scramble=True,seed).random_base2(m)`，同一2d点列拆列为A/B。`AB_i`为A替换第i列为B的对应列。响应均按声明物理范围映射后评估。

合并A/B响应均值为mean，`VarY=mean((combined-mean)^2)`，采用总体方差ddof=0：

- `S1_i=mean((YB-mean)*(YAB_i-YA))/VarY`，中心化避免响应平移改变指数。
- `ST_i=mean((YA-YAB_i)^2)/(2*VarY)`，采用Jansen总效应估计。

实际模型评估数为(d+2)n。零/非有限方差明确失败，不能伪造零指数。有限样本S1可为负、ST可大于1，原值保留并提示，不强行裁剪到[0,1]。ST−S1仅作为点估计差展示，微负不隐藏。基础n较小时提示采样误差风险；固定seed可复现，不等于误差已消失。本实现不构造置信区间或可证明的有限样本误差上界，不能将点估计当作CI。

### 手算与复现

独立U(0,1)的 `f=x+2y`：Morris EE分别1/2、σ理论0；Sobol S1/ST分别0.2/0.8。`f=xy`：S1分别3/7，ST分别4/7。响应加常数不改变指数。seed还包含这两个独立模型与范围，便于复验；实际浮点计算可能留下约1e−15的sigma。

NumPy采用float64；SQL中的系数、物理范围、响应均值/方差、各指数、EE与步长使用MySQL DOUBLE。完整模型、范围、参数、归一/物理轨迹与输出另存JSON快照并附SHA256；JSON数值不经Float32转换。科学输入不可原地修改，模型PATCH仅允许说明字段，因此同一研究可复跑并保留相同结果。重建新版本使用新模型/空间/研究。

## 快速启动

```sh
cp .env.example .env
docker compose config --quiet
docker compose up -d --build --wait
docker compose exec backend python scripts/seed_demo.py
```

前端 http://localhost:18233，后端 http://localhost:19233/docs，健康检查 `/health`；MySQL端口17733、库/用户名sensitivity、演示密码sensitivity_demo。

账号 `admin@sensitivity.demo`、`analyst@sensitivity.demo`、`viewer@sensitivity.demo`，统一密码 `FactorDemo2026!`。seed固定自然ID、只补缺，不覆盖用户说明；初次启动 `SEED_DEMO=true` 自动执行。基线运行由seed直接预计算，新建运行真实进入Redis后台worker。

```sh
docker compose ps
docker compose logs worker
docker compose down -v --remove-orphans
```

最后一条会清除本项目演示数据卷。

## 技术与目录

|部分|版本/职责|
|---|---|
|前端|Vue3.5.13、TypeScript5.7.2、Vite6、原生SVG、hash路由|
|后端|Python3.12、FastAPI0.115.6、SQLAlchemy2、PyJWT、PBKDF2|
|算法|NumPy2.2.1、SciPy1.14.1|
|存储/任务|MySQL8.4（验收8.4.11）、Redis7.4列表队列|
|容器|frontend/Nginx1.28、backend、worker、db、redis，恰好五服务|

`backend/src/{models,schemas,services,controllers,routes}`贯穿六聚合；`middlewares`处理审计与全局错误，`utils`处理JWT/PBKDF2/队列；`backend/scripts/seed_demo.py`负责自然键幂等seed。`backend/migrations`记录新库初始化方式；已有生产库需单独审查增量迁移。

`frontend/src/{api,stores,types,components/common,hooks,pages,router,utils,constants}`拆分职责。所有模型计算、业务校验与持久化在Python，前端仅作输入、选择和绘制真实结果。

前端本地开发：`cd frontend && npm ci && npm run dev`，Vite将 `/api` 代理到localhost:19233。后端本地开发创建Python3.12虚拟环境，安装 `backend/requirements.txt`，设置数据库/Redis/JWT变量，在backend目录启动 `uvicorn src.main:app --reload` 和另一个 `python -m src.worker` 进程；数据库与Redis可继续使用Compose服务。

|环境变量|用途/默认|
|---|---|
|COMPOSE_PROJECT_NAME|factor-sensitivity，隔离容器、卷与网络|
|FRONTEND_PORT/BACKEND_PORT/DB_PORT|18233/19233/17733|
|JWT_SECRET|本地演示值；部署替换|
|SEED_DEMO|true，自动补齐演示数据|
|DATABASE_URL/REDIS_URL|Compose内服务地址；本地开发按实际地址设置|

JWT未认证401，角色不足403，缺实体404，名称重复或状态冲突409，非法输入422；后端全局错误提供可恢复提示。审计记录写入路径、方法、响应码、认证账号，不记录密码/Token/模型正文。单worker无分布式任务重试保证，失败任务保留原因，可重新执行。

共享枚举：`backend/src/constants/enums.py` 与 `frontend/src/constants/enums.ts` 定义角色、运行状态、复核状态。认证、任务/复核服务以及前端权限与状态显示使用同一组取值；枚举定义不参与数值估计。

测试、截图、日志与TESTING放在同批 `test-artifacts/gb-2404/`，源码不混入测试产物。依赖通过npm ci锁定，`.env`、node_modules、构建产物与日志被忽略。

## License

MIT，见LICENSE。客户、数据和模型均为模拟。
