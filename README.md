## 知识图谱推理-斑马问题与逻辑问答系统

### 实验要求
- 使用`RDF`框架
- 需显示**每一步推理对应的规则**
- 可人工处理自然语言进行符号化输入
- 需支持推理规则的人工定义和修改，以支持斑马问题的**各种变种**
- 实现基于`FOIL`的归纳推理，并结合基于逻辑的演绎推理

### 使用方法
斑马问题无法使用**FOIL**算法求解，提供了两个知识图谱: `familyProblem` 和 `clanProblem`

在 `src` 文件夹下执行main.py，通过参数 `--kngraph` 指定知识图谱，如：

    python main.py --kngraph clanProblem


