# 飞书消息格式规范

## 输出规则

Pipeline 跑完后，**先在飞书创建文档**，然后可以发一条精简速览给用户。

## 速览格式（富文本 post）

使用 `feishu_im_user_message` 的 `msg_type=post`，格式：分割线 + emoji 分区

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "🔋 {化学式} 材料评估速览",
        "content": [
          [{"tag": "text", "text": "━━━━━━━━━━━━━━"}],
          [{"tag": "text", "text": "📊 核心结果"}],
          [{"tag": "text", "text": "• 预测电导率: {X} S/cm"}],
          [{"tag": "text", "text": "• 真实实验值: {X} S/cm (如有)"}],
          [{"tag": "text", "text": "• 误差: {X}% (如有)"}],
          [{"tag": "text", "text": ""}],
          [{"tag": "text", "text": "🏗️ 晶体结构"}],
          [{"tag": "text", "text": "• 空间群: {符号} (No. {编号})"}],
          [{"tag": "text", "text": "• 晶胞参数: a={X}, b={X}, c={X}"}],
          [{"tag": "text", "text": ""}],
          [{"tag": "text", "text": "📚 数据来源"}],
          [{"tag": "text", "text": "• OBELiX ID: {id} (如有)"}],
          [{"tag": "a", "text": "🔗 Materials Project", "href": "https://next-gen.materials..."}, "tag": "text", "text": " (如有)"}]
        ]
      }
    }
  }
}
```
