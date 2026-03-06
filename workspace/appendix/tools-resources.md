# 附录：工具与资源指南

> 本附录为AI基础设施从业者提供实用的工具、厂商产品、学习资源和参考资料汇总，助力从理论到实践的转化。

---

## A.1 开源工具清单

### A.1.1 资源调度与编排

| 工具名称 | 核心功能 | 适用场景 | 技术栈 | 社区活跃度 |
|---------|---------|---------|--------|-----------|
| **Kubernetes** | 容器编排、自动扩缩容 | 通用云原生工作负载 | Go | ⭐⭐⭐⭐⭐ |
| **Volcano** | 批处理调度、GPU感知调度 | AI/ML训练任务 | Go | ⭐⭐⭐⭐ |
| **YuniKorn** | 多租户资源调度、队列管理 | 大规模共享集群 | Go | ⭐⭐⭐ |
| **Slurm** | HPC作业调度、GPU集群管理 | 超算中心、科研集群 | C | ⭐⭐⭐⭐⭐ |
| **KubeRay** | Ray on K8s原生集成 | 分布式AI训练/推理 | Go/Python | ⭐⭐⭐⭐ |
| **Run:AI** | GPU虚拟化、动态分配 | 企业级GPU池化管理 | Go | 商业软件 |

**选型建议**：
- **小规模AI团队**：Kubernetes + Volcano组合
- **科研/高校环境**：Slurm + Pyxis/Enroot容器支持
- **多租户云平台**：YuniKorn + Gang Scheduling
- **Ray生态用户**：KubeRay提供最佳体验

### A.1.2 存储系统

| 工具名称 | 存储类型 | 性能特点 | 适用场景 |
|---------|---------|---------|---------|
| **Ceph** | 分布式对象/块/文件存储 | 强一致性、高可用 | 通用企业存储 |
| **MinIO** | 高性能对象存储 | S3兼容、性能优异 | AI数据湖、备份 |
| **JuiceFS** | 云原生分布式文件系统 | POSIX兼容、缓存加速 | 大规模AI训练 |
| **Alluxio** | 数据编排层 | 跨存储统一访问、缓存 | 多源数据整合 |
| **BeeGFS** | 并行文件系统 | 高并发、低延迟 | HPC/AI混合负载 |
| **Lustre** | 大规模并行文件系统 | 极高吞吐 | 超大规模训练集群 |

**性能对比**（典型配置下的顺序读写）：

| 系统 | 读吞吐 | 写吞吐 | IOPS | 扩展性 |
|------|--------|--------|------|--------|
| Lustre | 1TB/s+ | 800GB/s+ | 数百万 | 极强 |
| BeeGFS | 500GB/s | 400GB/s | 高 | 强 |
| JuiceFS | 取决于后端 | 取决于后端 | 中等 | 强 |
| Ceph | 200GB/s | 150GB/s | 中等 | 强 |

### A.1.3 监控与可观测性

| 工具名称 | 监控维度 | 核心特性 | 集成复杂度 |
|---------|---------|---------|-----------|
| **Prometheus** | 指标采集 | 时序数据库、PromQL查询 | 低 |
| **Grafana** | 可视化 | 丰富仪表板、告警 | 低 |
| **DCGM** | NVIDIA GPU监控 | GPU利用率、显存、温度 | 低 |
| **Weights & Biases** | ML实验追踪 | 训练可视化、模型版本 | 中 |
| **MLflow** | ML生命周期 | 实验管理、模型注册 | 中 |
| **TensorBoard** | 训练可视化 | 内置TensorFlow/Keras | 低 |
| **Jaeger** | 分布式追踪 | 链路追踪、性能分析 | 中 |

**GPU监控栈推荐组合**：
```
DCGM Exporter → Prometheus → Grafana Dashboard
                ↓
         自定义告警规则
                ↓
         PagerDuty/OpsGenie
```

### A.1.4 CI/CD与MLOps

| 工具名称 | 功能定位 | 核心能力 | 适用规模 |
|---------|---------|---------|---------|
| **GitLab CI** | 代码CI/CD | 集成DevOps全链路 | 中小团队 |
| **Jenkins** | 自动化服务器 | 插件丰富、高度可定制 | 大型企业 |
| **GitHub Actions** | 云原生CI/CD | 与GitHub深度集成 | 开源/小型 |
| **Argo Workflows** | K8s原生工作流 | 声明式DAG、容器化 | 云原生团队 |
| **Kubeflow** | 端到端ML平台 | Pipeline、Serving、Notebook | 企业级AI |
| **MLflow** | ML生命周期 | 跟踪、部署、注册 | 全规模 |
| **Tekton** | K8s CI/CD框架 | 标准化、可组合 | 平台团队 |

**MLOps流水线参考架构**：
```
代码提交 → 构建镜像 → 单元测试 → 数据验证
    ↓                              ↓
模型训练 ← 超参调优 ← 实验追踪 ← 数据准备
    ↓
模型评估 → 模型注册 → 审批 → 部署上线
    ↓                              ↓
性能监控 ← A/B测试 ← 影子部署 ← 金丝雀发布
```

### A.1.5 网络与通信

| 工具/库 | 功能 | 应用场景 |
|--------|------|---------|
| **RDMA Core** | RDMA用户态库 | InfiniBand/RoCEv2应用 |
| **NCCL** | NVIDIA集合通信 | GPU间P2P通信 |
| **UCX** | 统一通信框架 | 跨网络协议通信 |
| **MPI** | 消息传递接口 | 分布式并行计算 |
| **gRPC** | 高性能RPC | 微服务通信 |
| **DPDK** | 数据平面开发套件 | 高性能网络包处理 |

### A.1.6 推理服务与模型部署

| 工具名称 | 框架支持 | 核心特性 | 部署模式 |
|---------|---------|---------|---------|
| **Triton Inference Server** | TensorRT/ONNX/PyTorch | 多框架、动态批处理、GPU共享 | K8s/Docker |
| **vLLM** | PyTorch | PagedAttention、高吞吐 | 独立服务 |
| **TensorRT-LLM** | TensorRT | NVIDIA优化、极致性能 | GPU推理 |
| **Text Generation Inference** | PyTorch/ Safetensors | HuggingFace生态、Rust核心 | 容器化 |
| **Seldon Core** | 多框架 | K8s原生、A/B测试、金丝雀 | K8s CRD |
| **KServe** | 多框架 | 标准推理协议、自动扩缩 | K8s |

**推理框架选型矩阵**：

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 高吞吐LLM | vLLM/TensorRT-LLM | PagedAttention优化 |
| 多模型服务 | Triton | 统一入口、资源隔离 |
| 快速原型 | HF TGI | 开箱即用 |
| 企业级部署 | KServe/Seldon | 完整的MLOps支持 |

---

## A.2 厂商产品对比表

### A.2.1 GPU/加速计算产品

| 厂商 | 产品系列 | 旗舰型号 | 显存 | 算力(FP16) | 互联技术 | 适用场景 |
|------|---------|---------|------|-----------|---------|---------|
| **NVIDIA** | Hopper/B200 | H200/B200 | 141GB/192GB | 1979/4500 TFLOPS | NVLink 5 | 训练/推理 |
| **AMD** | Instinct MI300 | MI300X | 192GB HBM3 | 1300 TFLOPS | Infinity Fabric | 训练/推理 |
| **Intel** | Gaudi/Max | Gaudi3/Max 1550 | 128GB | 峰值性能 | xCCL | 训练为主 |
| **华为** | Ascend | 910B/910C | 64GB/96GB | 376 TFLOPS | HCCS | 国产化替代 |
| **天数智芯** | 天垓 | BI-V150 | 64GB | - | - | 训练/推理 |
| **海光** | 深算 | DCU Z100 | 32GB | - | - | 推理为主 |

**AI训练GPU对比（2025年主流）**：

| 指标 | H100 SXM | H200 SXM | MI300X | 910B |
|------|---------|---------|--------|------|
| FP8算力 | 3958 TF | 3958 TF | 2610 TF | 376 TF |
| FP16算力 | 1979 TF | 1979 TF | 1300 TF | 376 TF |
| 显存容量 | 80GB | 141GB | 192GB | 64GB |
| 显存带宽 | 3.35 TB/s | 4.8 TB/s | 5.3 TB/s | 1.6 TB/s |
| TDP | 700W | 700W | 750W | 400W |
| 制程工艺 | 4nm | 4nm | 5nm | 7nm |

### A.2.2 网络互联方案

| 厂商 | 产品名称 | 技术类型 | 单端口带宽 | 典型应用 |
|------|---------|---------|-----------|---------|
| **NVIDIA** | InfiniBand NDR | IB网络 | 400Gb/s | DGX SuperPOD |
| **NVIDIA** | Spectrum-X | 以太网 | 400Gb/s | AI以太网集群 |
| **Cisco** | Nexus 9000 | 以太网 | 400Gb/s | 通用AI网络 |
| **Arista** | 7060X5 | 以太网 | 400Gb/s | 超大规模AI |
| **H3C** | S12500R | 以太网 | 400Gb/s | 国产AI网络 |
| **华为** | CloudEngine | 以太网 | 400Gb/s | 昇腾集群 |
| **Intel** | IPU | 基础设施处理 | - | 计算卸载 |
| **Marvell** | OCTEON | DPU | - | 网络加速 |

**网络方案对比**：

| 特性 | InfiniBand NDR | RoCEv2 | Spectrum-X | UEC |
|------|---------------|--------|------------|-----|
| 延迟 | <1μs | 1-2μs | 1-2μs | <1μs(目标) |
| 带宽 | 400Gb/s | 400Gb/s | 400Gb/s | 800Gb/s |
| 拥塞控制 | 硬件级 | PFC/ECN | 智能调整 | 多路径喷洒 |
| 管理复杂度 | 低 | 中 | 中 | 低 |
| 开放性 | 封闭 | 开放 | NVIDIA生态 | 开放标准 |

### A.2.3 云服务AI平台

| 厂商 | 平台名称 | 核心优势 | 特色服务 |
|------|---------|---------|---------|
| **阿里云** | PAI灵骏 | 完整AI工程链 | 模型广场、Serverless推理 |
| **华为云** | ModelArts | 昇腾生态集成 | 盘古大模型服务 |
| **腾讯云** | TI平台 | 游戏/社交场景 | 向量数据库、图计算 |
| **AWS** | SageMaker | 全球基础设施 | 全托管、AutoML |
| **Azure** | AI Studio | 企业级集成 | OpenAI服务原生 |
| **GCP** | Vertex AI | 数据科学整合 | BigQuery无缝集成 |

**国内云平台AI能力对比**：

| 能力维度 | 阿里云PAI | 华为云ModelArts | 腾讯云TI |
|---------|-----------|-----------------|---------|
| 训练框架 | 全支持 | MindSpore优化 | 全支持 |
| 推理优化 | Blade | MindIE | Turbo |
| 模型仓库 | ModelScope | 自研 | 自研 |
| Serverless | 支持 | 支持 | 部分支持 |
| 国产GPU | 适配中 | 昇腾原生 | 适配中 |
| 价格竞争力 | 中 | 高(昇腾) | 中 |

### A.2.4 液冷解决方案

| 厂商 | 方案类型 | 功率密度支持 | 核心优势 | 代表产品 |
|------|---------|-------------|---------|---------|
| **CoolIT** | 冷板式 | 100kW/柜 | 技术成熟、部署广 | CHx80 |
| **Vertiv** | 冷板+浸没 | 250kW/柜 | 全产品线 | CoolChip |
| **绿色云图** | 浸没式 | 200kW/柜 | 国产浸没领先 | 浸没液冷系统 |
| **浪潮** | 冷板式 | 130kW/柜 | 整机柜方案 | i24液冷 |
| **曙光** | 冷板式 | 100kW/柜 | 超算经验 | TC4600E-LP |
| **英维克** | 模块化 | 150kW/柜 | 快速部署 | XRow |

**液冷技术对比**：

| 指标 | 冷板式 | 浸没式 | 喷淋式 |
|------|--------|--------|--------|
| 散热效率 | 中高 | 极高 | 高 |
| 改造成本 | 中 | 高 | 中高 |
| 维护难度 | 低 | 中 | 中 |
| 冷却液要求 | 低 | 高 | 中 |
| 适用功率密度 | <80kW | >100kW | 80-150kW |
| 成熟程度 | 成熟 | 快速发展 | 新兴 |

---

## A.3 学习资源推荐

### A.3.1 必读书籍

#### 基础理论类
| 书名 | 作者 | 出版年份 | 推荐理由 |
|------|------|---------|---------|
| 《深度学习》 | Goodfellow等 | 2016 | AI圣经，理论基础必读 |
| 《机器学习系统》 | 许斌等 | 2023 | 系统视角看ML工程 |
| 《设计数据密集型应用》 | Martin Kleppmann | 2017 | 分布式系统经典 |
| 《云计算：概念、技术与架构》 | Thomas Erl | 2013 | 云基础架构入门 |

#### 工程实践类
| 书名 | 作者/机构 | 出版年份 | 核心内容 |
|------|----------|---------|---------|
| 《Kubernetes in Action》 | Marko Lukša | 2022 | K8s权威指南 |
| 《MLOps工程实践》 | 陈玉基等 | 2023 | 机器学习工程化 |
| 《AI基础设施架构指南》 | 行业专家合著 | 2024 | 中文AI Infra专著 |
| 《大规模分布式存储系统》 | 杨传辉 | 2020 | 存储架构必读 |

#### 架构设计类
| 书名 | 作者 | 出版年份 | 适用读者 |
|------|------|---------|---------|
| 《数据密集型应用系统设计》 | Martin Kleppmann | 2017 | 系统架构师 |
| 《云原生架构白皮书》 | CNCF | 持续更新 | 云原生工程师 |
| 《AI原生应用架构》 | 阿里云 | 2024 | AI架构师 |

### A.3.2 在线课程

#### 平台课程
| 课程名称 | 平台 | 讲师/机构 | 难度 | 时长 |
|---------|------|----------|------|------|
| MLOps专项课程 | Coursera | DeepLearning.AI | 中级 | 4个月 |
| Kubernetes管理员认证 | Coursera | Linux Foundation | 中高级 | 3个月 |
| Stanford CS329S | Stanford Online | Chip Huyen | 高级 | 自学 |
| 大模型技术实战 | 极客时间 | 李沐团队 | 中高级 | 40课时 |
| AI基础设施工程师 | 慕课网 | 工业界专家 | 中级 | 60课时 |

#### 免费资源
| 资源名称 | 来源 | 内容类型 | 链接 |
|---------|------|---------|------|
| Full Stack Deep Learning | FSDL | 课程+项目 | fsdl.org |
| Made With ML | Goku Mohandas | 教程+代码 | madewithml.com |
| ML Systems Design | Chip Huyen | 文章+播客 | ml-systems-design.com |
| 李沐论文精读 | B站 | 视频讲解 | 搜索"跟李沐学AI" |

### A.3.3 技术会议与活动

#### 顶级学术会议
| 会议名称 | 领域 | 时间 | 重要度 |
|---------|------|------|--------|
| **NeurIPS** | 机器学习 | 12月 | ⭐⭐⭐⭐⭐ |
| **ICML** | 机器学习 | 7月 | ⭐⭐⭐⭐⭐ |
| **OSDI/SOSP** | 系统 | 轮流 | ⭐⭐⭐⭐⭐ |
| **ASPLOS** | 体系结构 | 3月 | ⭐⭐⭐⭐ |
| **MLSys** | ML系统 | 5月 | ⭐⭐⭐⭐⭐ |

#### 行业大会
| 会议名称 | 主办方 | 时间 | 侧重点 |
|---------|--------|------|--------|
| **GTC** | NVIDIA | 3月/秋季 | GPU生态 |
| **OCP Global Summit** | Meta | 10月 | 开放计算 |
| **KubeCon** | CNCF | 多地区 | 云原生 |
| **阿里云峰会** | 阿里云 | 多场次 | 国内AI云 |
| **华为全联接大会** | 华为 | 9月 | 昇腾生态 |

#### 线上社区
| 社区名称 | 平台 | 特色 | 活跃度 |
|---------|------|------|--------|
| **Papers with Code** | 网站 | 论文+代码 | 极高 |
| **Hugging Face** | 网站/Discord | 模型社区 | 极高 |
| **Reddit r/MachineLearning** | Reddit | 讨论区 | 高 |
| **InfoQ AI前线** | 网站/公众号 | 中文资讯 | 高 |
| **机器之心** | 网站/公众号 | 中文技术 | 高 |
| **AI Infrastructure Alliance** | Slack | 从业者交流 | 中 |

### A.3.4 重要博客与资讯源

| 来源 | 类型 | 更新频率 | 特色 |
|------|------|---------|------|
| **Google AI Blog** | 官方博客 | 月更 | 研究前沿 |
| **NVIDIA Technical Blog** | 技术博客 | 周更 | 工程实践 |
| **Chip Huyen's Newsletter** | 个人博客 | 月更 | 系统设计 |
| **The Batch** | 邮件列表 | 周更 | AI行业动态 |
| **Import AI** | 邮件列表 | 周更 | 技术趋势 |
| **OneFlow** | 技术博客 | 周更 | 中文深度 |
| **阿里技术** | 官方博客 | 周更 | 工程实践 |

---

## A.4 术语表（Glossary）

### A.4.1 计算相关术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **AI加速卡** | AI Accelerator | 专为AI计算优化的处理器，如GPU、TPU、NPU等 |
| **张量核心** | Tensor Core | NVIDIA GPU中专用于矩阵运算的专用单元 |
| **混合精度训练** | Mixed Precision Training | 同时使用FP16和FP32进行训练，平衡速度与精度 |
| **模型并行** | Model Parallelism | 将模型不同层分布到多个设备上 |
| **数据并行** | Data Parallelism | 将数据分片，每个设备处理不同批次 |
| **流水线并行** | Pipeline Parallelism | 将模型按阶段划分，形成处理流水线 |
| **张量并行** | Tensor Parallelism | 将单层内的张量计算拆分到多个设备 |
| **专家并行** | Expert Parallelism | MoE模型中不同专家分布在不同设备 |
| **分布式数据并行** | DDP | PyTorch的分布式训练原语 |
| **完全分片数据并行** | FSDP | 将模型参数、梯度和优化器状态分片 |

### A.4.2 网络与互联术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **NVLink** | NVIDIA NVLink | NVIDIA专有的高速GPU互联技术 |
| **InfiniBand** | InfiniBand | 高性能计算网络标准 |
| **RoCE** | RDMA over Converged Ethernet | 在以太网上实现RDMA |
| **RDMA** | Remote Direct Memory Access | 绕过CPU直接访问远程内存 |
| **Scale-Up** | Scale-Up | 纵向扩展，单节点内增加资源 |
| **Scale-Out** | Scale-Out | 横向扩展，增加节点数量 |
| **超节点** | SuperNode | 高速互联的多GPU节点，形成统一计算域 |
| **CPO** | Co-Packaged Optics | 光引擎与交换芯片共封装技术 |
| **DPU** | Data Processing Unit | 数据处理单元，卸载网络/存储任务 |
| **智算网络** | AI Computing Network | 面向AI负载优化的数据中心网络 |

### A.4.3 存储术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **HBM** | High Bandwidth Memory | 高带宽内存，3D堆叠封装 |
| **CXL** | Compute Express Link | 计算快速链接，内存扩展协议 |
| **内存池化** | Memory Pooling | 将分散内存资源池化共享 |
| **并行文件系统** | Parallel File System | 支持并发访问的高性能文件系统 |
| **对象存储** | Object Storage | 扁平化数据存储架构 |
| **检查点** | Checkpoint | 训练过程中的状态保存点 |
| **数据湖** | Data Lake | 原始格式存储的大规模数据仓库 |

### A.4.4 AI/ML术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **Transformer** | Transformer | 基于自注意力机制的神经网络架构 |
| **MoE** | Mixture of Experts | 混合专家模型，稀疏激活架构 |
| **KV Cache** | Key-Value Cache | 大模型推理中的键值缓存 |
| **TTFT** | Time To First Token | 首Token生成时间，衡量响应速度 |
| **TPOT** | Time Per Output Token | 每输出Token时间，衡量生成速度 |
| **吞吐量** | Throughput | 单位时间处理的请求/Token数量 |
| **批处理大小** | Batch Size | 单次前向传播处理的样本数 |
| **连续批处理** | Continuous Batching | 动态组批，提升GPU利用率 |
| **分页注意力** | PagedAttention | vLLM提出的内存优化技术 |
| **投机解码** | Speculative Decoding | 草稿模型加速解码技术 |

### A.4.5 运维与工程术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **MLOps** | Machine Learning Operations | 机器学习工程化运维 |
| **LLMOps** | Large Language Model Operations | 大模型运维实践 |
| **AIOps** | Artificial Intelligence for IT Operations | 智能运维 |
| **GitOps** | Git Operations | 以Git为核心的运维模式 |
| **IaC** | Infrastructure as Code | 基础设施即代码 |
| **SRE** | Site Reliability Engineering | 站点可靠性工程 |
| **可观测性** | Observability | 通过输出推断系统内部状态的能力 |
| **SLA** | Service Level Agreement | 服务等级协议 |
| **SLO** | Service Level Objective | 服务等级目标 |
| **PUE** | Power Usage Effectiveness | 数据中心能源使用效率 |

### A.4.6 新兴技术术语

| 术语 | 英文全称 | 定义 |
|------|---------|------|
| **Agentic AI** | Agentic AI | 具有自主性的AI Agent系统 |
| **MCP** | Model Context Protocol | 模型上下文协议（Anthropic提出） |
| **A2A** | Agent-to-Agent Protocol | Agent间通信协议（Google提出） |
| **RAG** | Retrieval-Augmented Generation | 检索增强生成 |
| **向量数据库** | Vector Database | 存储和检索向量嵌入的数据库 |
| **800VDC** | 800V Direct Current | 800伏直流供电架构 |
| **液冷** | Liquid Cooling | 使用液体进行散热的技术 |
| **Chiplet** | Chiplet | 芯粒，模块化芯片设计 |
| **CPO** | Co-Packaged Optics | 共封装光学技术 |

---

## A.5 参考文献

### 白皮书与技术报告

[1] NVIDIA. *NVIDIA DGX SuperPOD Deployment Guide* [EB/OL]. 2024. https://docs.nvidia.com/dgx/dgxsuperpod-deployment-guide/

[2] 新华三集团. *Agentic AI时代对基础架构的深度思考* [EB/OL]. 2025-11-14. https://www.h3c.com/cn/About_H3C/Company_Publication/Company_News/

[3] 阿里云. *AI原生应用架构白皮书* [R]. 2024.

[4] 华为云. *云原生AI技术架构白皮书* [R]. 2024.

[5] OpenAI. *OpenAI Infrastructure Blueprint* [R]. 2024.

[6] Meta. *Open Compute Project: AI/ML Hardware Design* [EB/OL]. https://www.opencompute.org/

[7] Ultra Ethernet Consortium. *UEC Specification v1.0* [S]. 2024.

[8] CXL Consortium. *Compute Express Link Specification v3.0* [S]. 2023.

### 学术论文

[9] Vaswani A, et al. *Attention Is All You Need* [C]. NeurIPS, 2017.

[10] Kaplan J, et al. *Scaling Laws for Neural Language Models* [J]. arXiv:2001.08361, 2020.

[11] Kwon W, et al. *Efficient Memory Management for Large Language Model Serving with PagedAttention* [C]. SOSP, 2023.

[12] Rajbhandari S, et al. *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models* [C]. SC, 2020.

[13] Shoeybi M, et al. *Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism* [J]. arXiv:1909.08053, 2019.

[14] Lepikhin D, et al. *GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding* [C]. ICLR, 2021.

### 技术博客与文章

[15] NVIDIA Developer Blog. *Optimizing GPU Performance for Deep Learning* [EB/OL]. 2024. https://developer.nvidia.com/blog/

[16] Google AI Blog. *Pathways: Asynchronous Distributed Dataflow for ML* [EB/OL]. 2022. https://ai.googleblog.com/

[17] Chip Huyen. *Machine Learning Systems Design* [M/OL]. 2022. https://ml-systems-design.com/

[18] Eugene Yan. *Patterns for Building LLM-based Systems & Products* [EB/OL]. 2023. https://eugeneyan.com/writing/llm-patterns/

### 开源项目文档

[19] Kubernetes. *Kubernetes Documentation* [EB/OL]. https://kubernetes.io/docs/

[20] Kubeflow. *Kubeflow Documentation* [EB/OL]. https://www.kubeflow.org/docs/

[21] NVIDIA. *Deep Learning Performance Guide* [EB/OL]. https://docs.nvidia.com/deeplearning/

[22] PyTorch. *Distributed Training Documentation* [EB/OL]. https://pytorch.org/docs/stable/distributed.html

[23] vLLM. *vLLM Documentation* [EB/OL]. https://docs.vllm.ai/

### 行业报告

[24] Gartner. *Market Guide for AI Infrastructure* [R]. 2024.

[25] IDC. *China AI Infrastructure Market Forecast* [R]. 2024.

[26] 信通院. *人工智能基础设施发展态势报告* [R]. 2024.

### 标准规范

[27] IEEE. *IEEE 802.3bs-2017: 200 Gb/s and 400 Gb/s Ethernet* [S]. 2017.

[28] InfiniBand Trade Association. *InfiniBand Architecture Specification* [S]. 2023.

[29] OCP. *Open Rack Specification v3.0* [S]. 2022.

---

## 附录更新说明

| 版本 | 日期 | 更新内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-03-06 | 初始版本，涵盖工具、厂商、学习资源和术语表 | AI写作团队 |

---

> 💡 **使用提示**：本附录内容将根据技术发展和社区反馈持续更新。如需补充新的工具或资源，请通过项目的Issue或PR提交建议。
