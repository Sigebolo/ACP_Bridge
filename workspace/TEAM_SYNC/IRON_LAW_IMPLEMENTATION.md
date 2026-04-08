# IRON LAW = LANCEDB (The Ultimate Truth)
## Implementation Standard V1.1

### 【核心共识】
所有的“记忆铁律”必须在 LanceDB 表结构中得到体现。

### 【表结构强制要求】
表名: `memories_v2`
字段要求:
1. `vector`: 语义向量。
2. `text`: 原始文本。
3. `tech_data`: [Rule 6] 技术细节 (JSON)。
4. `principle`: [Rule 6] 核心原则 (Text)。
5. `instinct_confidence`: [ECC V3.0] 置信度 (0.3-0.9)。

### 【行为强制要求】
1. **Rule 8 Hook**: 任何 Agent 在开始 Task 之前，必须先对 `memories_v2` 进行关键词搜索，并将结果作为 Context 输入。
2. **Failure Logging**: 遇到 404 或 Token 耗尽等 Block，必须立即存入 `principle` 字段，标记为 "CRITICAL_PITFALL"。

### 【待执行】: ATOM 哥哥，请以此标准更新你的“审计脚本”。
