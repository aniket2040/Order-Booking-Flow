| Module       | Scenario            | Expected              | Actual | Status |
| ------------ | ------------------- | --------------------- | ------ | ------ |
| Conversation | New session         | Session created       |        |        |
| Conversation | Existing session    | Same session reused   |        |        |
| Draft        | Draft created       | One draft             |        |        |
| Draft        | Draft persists      | Draft reused          |        |        |
| AI           | Intent extraction   | ORDER                 |        |        |
| AI           | Slot extraction     | Nike, Black, 2        |        |        |
| Workflow     | DetectIntent        | → CollectRequirements |        |        |
| Workflow     | CollectRequirements | saves slots           |        |        |
| Workflow     | ResolveProduct      | finds Nike            |        |        |
| Workflow     | ResolveVariant      | finds size            |        |        |
| Workflow     | Inventory           | validates stock       |        |        |
| Pricing      | totals              | correct               |        |        |
| Review       | summary             | correct               |        |        |
| Order        | create              | success               |        |        |
