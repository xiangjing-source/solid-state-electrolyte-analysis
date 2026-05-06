# Materials Project API 使用注意事项

## Python 版本问题

**macOS 系统 Python 3.9** 使用 LibreSSL 2.8.3，与 MP API 的 TLS 不兼容，间歇性 SSL 握手失败（SSLEOFError）。curl 同样受影响。

**解决方案**: 使用 Miniconda + Python 3.10.20（自带 OpenSSL）

```bash
# 激活 lizy 环境
export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897
PY=$HOME/miniconda3/envs/lizy/bin/python
```

## MP API 调用前必须加的 Patch

Python 3.10 缺少 `typing.NotRequired`，需要手动补丁：

```python
import typing
if not hasattr(typing, 'NotRequired'):
    import typing_extensions
    typing.NotRequired = typing_extensions.NotRequired
```

## emmet-core 兼容性

`emmet-core` 的 `outcar_adapter.py` 可能报 NotRequired 错误，已打补丁。注意：`pip upgrade emmet-core` 会覆盖补丁，需重新打。

## 代理设置

conda 和网络请求都需要显式设置代理：

```bash
export http_proxy=http://127.0.0.1:7897 https_proxy=http://127.0.0.1:7897
```

系统代理设置（网络偏好设置）不会被 conda 自动继承。

## API Key 位置

`~/.mp_api_key` 或环境变量 `MP_API_KEY`

## MP 中不存在的材料

以下材料在 Materials Project 中没有收录：
- Li₂ZrCl6（Li-Zr-Cl 三元体系整个不在 MP）
- Li₉N₂Cl3（Li-N-Cl 体系也不在）

查询不到时应在报告中说明"MP 暂无收录"。
