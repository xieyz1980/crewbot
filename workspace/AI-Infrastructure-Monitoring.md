# AI基础设施资源监控笔记

**监控目标**: 三大AI基础设施厂商官方资源
**更新频率**: 每周检查一次
**最后更新**: 2025-03-05

---

## 📌 监控网站列表

### 1. NVIDIA 数据中心资源
**URL**: https://www.nvidia.cn/data-center/resources/

**核心内容**:
- NGC (NVIDIA GPU Cloud) - GPU优化的深度学习、机器学习软件中心
- GPU加速应用目录 - 700+针对GPU优化的应用
- 面向IT专业人士的AI课程 (Deep Learning Institute)
- 数据中心GPU产品文档
- Blackwell/Hopper架构技术资源

**关键资源**:
- Blackwell资源中心
- 数据中心GPU资源中心
- MLPerf基准测试
- NVIDIA认证系统目录
- 能效计算器

---

### 2. AWS AI基础设施
**URL**: https://aws.amazon.com/cn/ai/infrastructure/

**核心内容**:
- **训练芯片**: AWS Trainium (低成本训练)
- **推理芯片**: AWS Inferentia (高性能推理)
- **实例类型**:
  - EC2 Trn1/Trn2 - 训练实例
  - EC2 Inf1/Inf2 - 推理实例  
  - EC2 P5 - GPU训练实例 (H100)
  - EC2 G5 - GPU推理实例 (A10G)
- **托管服务**: Amazon SageMaker AI
- **容器服务**: Amazon EKS/ECS with GPU支持

**最新动态 (2025-03)**:
- Amazon EC2 Trn2实例和UltraServers
- Amazon EC2 Trn3 UltraServer
- Amazon EC2 P6e-GB300 UltraServers
- AWS AI工厂

**客户案例**:
- Perplexity: 使用SageMaker HyperPod训练速度提升40%
- Vyond: 使用Inferentia成本降低20%
- Anthropic: 使用Trainium/Inferentia构建模型

---

### 3. IBM AI基础设施
**URL**: https://www.ibm.com/think/topics/ai-infrastructure

**核心内容**:
- **AI基础设施定义**: 支持AI应用开发和部署的硬件软件栈
- **vs传统IT基础设施**: 需要GPU/TPU而非CPU，低延迟云环境
- **四大核心组件**:
  1. 数据存储与处理
  2. 计算资源 (GPU/TPU)
  3. 机器学习框架 (TensorFlow/PyTorch)
  4. MLOps平台

**六大优势**:
1. 可扩展性与灵活性
2. 性能与速度
3. 协作效率
4. 合规性
5. 成本优化
6. 生成式AI能力

**建设六步法**:
1. 定义预算与目标
2. 选择合适硬件软件
3. 找到合适网络方案
4. 决定云/本地部署
5. 建立合规措施
6. 实施与维护

**相关产品**:
- IBM Storage Fusion (混合云容器存储)
- IBM z17 (企业级AI主机)
- IBM Telum处理器

---

## 📊 厂商对比

| 维度 | NVIDIA | AWS | IBM |
|------|--------|-----|-----|
| **核心优势** | GPU硬件+软件生态 | 云服务广度+自研芯片 | 企业级混合云+主机 |
| **AI芯片** | GPU (H100/Blackwell) | Trainium/Inferentia | Telum处理器 |
| **训练方案** | DGX系统 | EC2 Trn/P系列 | IBM z17 |
| **推理方案** | Triton推理服务器 | EC2 Inf系列+SageMaker | IBM Storage Fusion |
| **软件栈** | CUDA/TensorRT/NGC | SageMaker/Bedrock | Watsonx |
| **目标客户** | 开发者和研究人员 | 云原生企业 | 大型传统企业 |

---

## 🔄 监控检查清单

### 每周检查项
- [ ] NVIDIA: 检查NGC新容器/模型
- [ ] NVIDIA: 查看Blackwell架构更新
- [ ] AWS: 检查新实例类型发布
- [ ] AWS: 查看Trainium/Inferentia更新
- [ ] IBM: 查看AI Academy新课程
- [ ] IBM: 检查z17/Storage Fusion更新

### 每月深度检查
- [ ] 收集新白皮书/技术报告
- [ ] 整理客户案例更新
- [ ] 对比厂商新功能
- [ ] 更新知识库

---

## 💡 学习要点

### 当前热点 (2025 Q1)
1. **新一代AI芯片**
   - NVIDIA Blackwell架构
   - AWS Trainium2/Inferentia2
   - 更高算力+更低成本

2. **超大规模集群**
   - UltraServers (AWS)
   - DGX SuperPOD (NVIDIA)
   - AI工厂概念

3. **企业级AI**
   - 混合云AI架构
   - 数据主权与合规
   - MLOps成熟度

4. **成本优化**
   - 训推分离架构
   - Spot实例+容量块
   - 能效计算

---

## 📁 关联资料

- 本地资料库: `/workspace/projects/AI-Infra-Materials-Notes.md`
- GitHub资料: https://github.com/xieyz1980/AI-Infra-Materials

---

*备注: 此笔记会随网站更新而更新*