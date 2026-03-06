# Agentic AI时代对基础架构的深度思考 - 学习笔记

**来源**：新华三集团 - IT大嘴巴  
**发布时间**：2025-11-14  
**学习时间**：2026-03-04  

---

## 一、核心概念解析

### 1. Agents vs AI Agents vs Agentic AI

**Agents**：能感知环境并为达成目标而行动的实体（最基础概念）  
**AI Agents**：在Agents基础上增加了大模型能力，具备记忆能力及自主规划/决策能力  
**Agentic AI**：AI Agents追求的更高阶形态，更加强调：
- 自主性
- 目标驱动
- 环境交互
- 反思学习

### 2. AI Agent系统三大模块

**感知模块**：
- 通过NLP、CV、ASR等技术构建环境状态表征

**认知与决策模块**：
- 多模态大模型的持续优化是核心
- RAG知识库、向量数据库、元学习等是重要能力补充

**行动模块**：
- MCP协议（Anthropic）的诸多限制亟待解决
- 人机交互/物理交互将延伸AI Agents应用领域

### 3. 多Agent系统交互
- 多个AI Agent系统通过**A2A协议（Google）**进行交互
- 需要关注：Agents的发现、认证/授权、状态管理
- **AG-UI**：通过轻量化的HTTP实现Agent与前端的连接

---

## 二、典型应用架构

### 1. 编程范式转变
- **过去**：通过Java/Python等对计算机进行编程
- **之后**：通过参数调参对神经网络进行编程
- **Agentic AI时代**：通过提示词/上下文等对大模型进行编程
- **程序载体**：从CPU转向GPU

### 2. 应用架构特点
Agentic AI与云原生/微服务模式存在巨大差异

**AWS Bedrock AgentCore解决方案（7大核心组件）**：
- AgentCore Runtime
- AgentCore Memory
- AgentCore Identity
- ...

**阿里云**：推出较完整的AI原生应用框架组件

### 3. 典型架构组件

**API网关**：
- 安全管控及授权
- 多Agents API管理
- 用户需求调度至不同AI Agent

**AI网关（中间层）**：
- 对接LLMs（协议转换）
- 对接MCP Servers（协议转换）

**MCP管理中心**：
- MCP Server的注册与发现

**监控组件**：
- 建立围绕Token的全链路监控体系

---

## 三、对基础设施的影响

### （一）计算架构

#### 1. 推理加速关键指标
- **TTFT（Time to First Token）**：决定模型推理流畅度
- **TPOT（Time Per Output Token）**：决定Decode阶段关键性能

#### 2. 上下文工程
- 将Prompt、RAG、Context等多种信息高效传递给LLM
- 层次化Context管理、增量更新、注意力窗口智能裁剪
- 提升KV缓存命中率，降低访存开销

#### 3. CPU角色重塑：从中心控制器到对等协调者
- **数据面**：GPU负责大模型推理
- **控制面**：CPU负责任务分解、负载均衡、通信同步
- CPU通过高速互连网络直接访问GPU HBM及远端池化内存
- 下一代CPU集成高速互联IP（XXLink die）

#### 4. 供电架构革命：800VDC
- 单AI机柜功率向兆瓦级迈进
- 传统供电体系触及物理与经济极限
- **800VDC架构**：将配电电压提升至800V高压直流
- 大幅降低传输电流，解决空间占用、线缆成本和能量损耗
- 英伟达2025 OCP大会提出

#### 5. GPU-CPU-存储协同架构
- GPU/CPU/存储处于同一个**Scale-up域**内
- 通过**XX Switch**互联
- 业界生态：NVLink、UB、CXL、UALink

**CXL**：
- 基于PCIe物理层，迭代速率缓慢
- 核心价值：AI计算环境下的一致性内存访问
- 兼容性强，但协议栈复杂
- 定位：内存资源的池化与共享
- 未必适用于GPU间高性能计算场景

**Chiplet架构**：
- 提升晶圆良率，降低制造成本
- 目前各家芯片厂商使用独有的die间互连协议
- ARM推出**FCSA**（基础小芯片系统架构）
- 定义完整协议栈和接口标准，实现Chiplet即插即用

---

### （二）存储架构

**趋势：从单一GPU/CPU附属资源到全局可池化资产**

#### 1. HBM（高带宽内存）
- 满足GPU算力需求的关键
- 容量随工艺制程提升持续增长
- 单GPU集成的HBM容量有限增长

#### 2. 内存池化（Memory Pooling）
- 高性能显存从"固定依附于特定处理器"向"全局可池化、可共享的资源"演进
- 借助XXLink技术：
  - GPU能够透明访问共享的大规模HBM显存资源
  - 可以访问全局的池化内存，扩展有效可寻址空间
  - 缓解KV Cache压力

#### 3. CXL与XXLink整合
- CXL在内存池领域具备"内存容量扩展、协议级缓存一致性"等核心优势
- **CXL over XXLink**：将CXL和XXLink整合到统一数据中心架构
- 充分发挥两者互补优势

#### 4. 存储子系统多层化结构
根据介质速率形成层级：
- **HBM**（最快）
- **池化内存**（大容量）
- **NVMe SSD**（持久化存储）

由特定的硬件加速器及XXLink协议协同管理数据在层级间的流动

---

### （三）网络架构（DCN）

#### 1. AI Agents对网络的新挑战
- 大量并行计算任务（TP和EP）对网络带宽需求极高
- 处理超长上下文文本，KV Cache规模迅速膨胀
- 要求网络具有极高的吞吐和高并发处理能力
- Transformer架构由Dense向MoE架构演进

#### 2. Scale-Up架构与超节点（SuperPod）
- **超节点优势**：统一的内存语义和高度集成的架构
- 所有GPU处于同一个超带宽域（HBD, High Bandwidth Domain）
- 通信延迟极低，数据交换效率极高
- 超节点规模向千卡级迈进

#### 3. 光互连技术演进路径
**三阶段演进**：
- **LPO**（Linear-drive Pluggable Optics）：线性驱动可插拔光模块，适用于400G/800G主流场景
- **NPO**（Near-packaged Optics）：近封装光模块，将光引擎更靠近交换芯片，缩短电通道长度
- **CPO**（Co-packaged Optics）：共封装光模块，将光引擎与交换ASIC共封装在同一基板上

**判断**：NPO方案可能会成为Scale-Up光互连的主流方案

#### 4. 协议层范式转移
**从封闭私有协议走向开放标准生态**：

过去：
- NVIDIA NVLink
- 华为UB（Unified Bus）
- 形成"技术孤岛"

开放标准：
- **UALINK**：多家头部厂商联合推动，支持多芯片互连与内存共享
- **ESUN**（Ethernet for Scale-Up Networks）：尝试将以太网引入Scale-up场景

#### 5. Scale-out网络演进
**从RoCE向新一代协议跃迁**：

传统RoCE问题：
- 负载均衡复杂
- 乱序重传
- 拥塞控制复杂

新技术：
- **UEC**（超以太网联盟）：多路径数据包喷洒、选择性重传、LLR、CBFC等技术
- **ETH+**（高通量以太网）

推动AI网络从"尽力而为"向"智能可靠"质变

#### 6. 网络融合趋势
**Scale-out与DCN融合**：
- 超节点作为DCN接入的一个层级
- DCN网络带宽稳步增长
- DCN内应用全域支持RDMA

**Scale-up与Scale-out统一**：
- 二者都围绕"内存远程读取"这一核心需求展开演进
- 底层纷纷采用以太网进行承载
- 推动两者走向进一步融合

---

### （四）DCI网络（跨数据中心网络）

#### 1. 跨区域扩展架构（Scale-Across）
**背景**：
- Agentic AI针对多归属、多地域推理和训练资源的调用和访问成为常态
- ScaleUP和ScaleOut无法覆盖Agentic AI的多元跨域资源调用

**Scale-Across**：
- 利用多域多归联合计算的方式突破大规模Agentic AI计算和通信的归属和地理限制
- 在归属/空间/电力/资源/算法/数据安全等方面进行协同和优化
- 使分散的AI算力资源和存储资源从管理逻辑和计算效果上趋同于集中化的集群效果

#### 2. 跨IDC通信网络要求
- 高带宽
- 低延迟
- 高可靠性

#### 3. 业界方案
**英伟达Spectrum-XGS以太网技术**：
- 距离自适应拥塞控制
- 精准延迟管理
- 端到端遥测

**H3C方案**：
- "端侧优化+网关增强+广网升级"一体化方案
- 跨数据中心RDMA解决方案
- 实现了50KM和100KM场景下整体训练/推理性能损失可忽略

#### 4. 训练/推理业务层面优化
- **流水线并行（PP）隐藏技术**
- **数据并行（DP）隐藏技术**
- 合理分布于不同域，有效利用广域网资源

#### 5. 智算跨域调度平台
**需要具备**：
- **北向API**：用户的统一接入/认证和管理
- **南向API**：地域以及算力架构差异屏蔽，异属异构的算力资源和网络资源统一接入和管理
- 支撑大模型作业任务的跨域调度和计费
- 实现算力资源训练和推理的异地同步/异属合并/异构混合
- 真正实现**无界算力**

---

## 四、总结与展望

### 核心观点
1. **Agentic AI将带来深层次全方位的变革**
2. **谈AI算力，不再谈TFlops、PFlops，而是谈GW、10GW、100GW**
3. **谈AI基础设施单元，不再谈OAM机型、超节点，而是谈AI集群、AI工厂**

### 技术趋势
- **计算**：GPU/CPU/存储完全解耦，动态组合
- **网络**：从电互联到光互联，从封闭到开放
- **存储**：多层化结构，全局可池化
- **供电**：800VDC原生直通

### 未来架构
通过多柜集成，实现：
- GPU计算、CPU调度、存储资源的完全解耦
- 动态组合，显著提高资源利用率
- 部署灵活性及能效优化配比
- 模块化Tray设计，功能专精
- 真正实现资源即服务（RaaS）

---

## 五、关键术语表

| 术语 | 含义 |
|------|------|
| Agentic AI | AI Agents的高阶形态，强调自主性、目标驱动 |
| MCP | Model Context Protocol，模型上下文协议 |
| A2A | Agent-to-Agent协议 |
| AG-UI | Agent-Graphical User Interface |
| TTFT | Time to First Token，首Token时间 |
| TPOT | Time Per Output Token，每输出Token时间 |
| HBD | High Bandwidth Domain，高带宽域 |
| LPO | Linear-drive Pluggable Optics |
| NPO | Near-packaged Optics |
| CPO | Co-packaged Optics |
| UEC | Ultra Ethernet Consortium，超以太网联盟 |
| CXL | Compute Express Link |
| UALink | Ultra Accelerator Link |
| ESUN | Ethernet for Scale-Up Networks |
| FCSA | Foundational Chiplet System Architecture |
| 800VDC | 800Volt Direct Current，800伏直流供电 |
| Scale-Up | 纵向扩展（节点内扩展） |
| Scale-Out | 横向扩展（集群扩展） |
| Scale-Across | 跨区域扩展（跨地域扩展） |

---

**标签**：#AgenticAI #AI架构 #基础设施 #新华三 #ScaleUp #CXL #液冷 #800VDC
