# AI基础设施资源周报 - 2026-03-05

**检查时间**: 2026-03-05 10:48:00
**检查人**: 小煤球（自动化脚本+人工整理）

---

## 🔍 检查网站

### 1. NVIDIA 数据中心资源
**URL**: https://www.nvidia.cn/data-center/resources/
**状态**: ✅ 已检查

**待确认更新项**:
- [x] NGC目录新容器/模型 - NGC持续提供GPU优化软件
- [x] Blackwell架构新文档 - Blackwell资源中心已上线
- [x] DGX/HGX产品更新 - HGX平台文档完善
- [ ] 新认证系统发布

**重要发现**:
- **NGC (NVIDIA GPU Cloud)**: 专为GPU优化的深度学习、机器学习和HPC软件中心，提供700+加速应用
- **Blackwell架构**: 新一代AI芯片架构，资源中心已开放
- **DLI课程**: 面向IT专业人士的AI课程，涵盖GPU计算、NVIDIA AI软件架构
- **认证系统**: NVIDIA认证系统目录持续更新

---

### 2. AWS AI基础设施
**URL**: https://aws.amazon.com/cn/ai/infrastructure/
**状态**: ✅ 已检查

**待确认更新项**:
- [x] 新EC2实例类型发布 - Trn2/Trn3已发布
- [x] Trainium/Inferentia更新 - Trainium2芯片已商用
- [ ] SageMaker新功能
- [x] 新客户案例 - Perplexity、Vyond、Anthropic案例

**重要发现**:
- **新实例发布**:
  - Amazon EC2 Trn2实例和UltraServers
  - Amazon EC2 Trn3 UltraServer
  - Amazon EC2 P6e-GB300 UltraServers (下一代GPU实例)
  
- **自研芯片进展**:
  - AWS Trainium2: 低成本训练芯片
  - AWS Inferentia2: 高性能推理芯片
  - AWS AI工厂: 专门用于AI训练的数据中心

- **客户成功案例**:
  - Perplexity: 使用SageMaker HyperPod训练速度提升40%
  - Vyond: 使用Inferentia2将生成式AI视频成本降低20%
  - Anthropic: 使用Trainium/Inferentia构建Claude模型

---

### 3. IBM AI基础设施
**URL**: https://www.ibm.com/think/topics/ai-infrastructure
**状态**: ✅ 已检查

**待确认更新项**:
- [ ] AI Academy新课程
- [x] IBM z17/Storage Fusion更新 - z17已发布
- [ ] 新白皮书/报告
- [ ] Think Newsletter内容

**重要发现**:
- **IBM z17**: 首款为AI时代设计的大型机，每秒24万亿次运算
- **AI基础设施六步法**: 
  1. 定义预算与目标
  2. 选择合适硬件软件
  3. 找到合适网络方案
  4. 决定云/本地部署
  5. 建立合规措施
  6. 实施与维护

- **核心组件**: 数据存储处理、计算资源(GPU/TPU)、ML框架、MLOps平台
- **IBM Storage Fusion**: 混合云容器原生存储平台

---

## 📊 本周重点

### 技术趋势
1. **超大规模AI集群成为标配**
   - AWS推出UltraServers概念
   - NVIDIA DGX SuperPOD持续演进
   - 单集群规模持续扩大

2. **训推分离架构普及**
   - AWS Trainium用于训练，Inferentia用于推理
   - 成本优化成为核心诉求
   - Perplexity/Vyond案例证明ROI显著

3. **企业级AI基础设施成熟**
   - IBM z17将AI能力带入主机
   - 混合云AI架构成为主流
   - 合规与数据主权受重视

### 产品发布
- **AWS EC2 P6e-GB300**: 基于下一代GPU的实例
- **AWS Trn3 UltraServer**: 新一代训练服务器
- **IBM z17**: AI原生大型机

### 客户案例
- **Perplexity**: SageMaker HyperPod提升训练速度40%
- **Vyond**: Inferentia2降低视频生成成本20%
- **Deutsche Telekom**: 使用Inferentia2部署大语言模型

---

## 📝 行动项

- [x] 深入学习新内容 - 已完成初步学习
- [ ] 更新知识库 - 待更新AI-Infra-Materials-Notes.md
- [ ] 应用到简历/面试准备 - 将新案例加入简历

---

## 💡 给你的建议

根据今天的监控结果，建议你关注：

1. **AWS Trainium/Inferentia**: 这是你简历中AWS技能的补充，可以强调成本优化能力
2. **IBM z17**: 如果有金融/电信行业面试，了解企业级AI主机有加分
3. **Perplexity案例**: 很好的谈资，说明你对前沿AI公司技术栈的了解
4. **UltraServers/AI工厂**: 了解超大规模AI集群架构，适合AI架构师面试

---

*报告生成时间: 2026-03-05*
