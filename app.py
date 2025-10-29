import streamlit as st
import requests

st.set_page_config(page_title="GitHub JSON Search", page_icon="🔎", layout="centered")
st.title("🔎 GitHub JSON Search (link-based)")

# 说明：将下面这个 RAW_URL 替换为你的 GitHub 仓库中 JSON 文件的 raw 链接
# 例子：https://raw.githubusercontent.com/JingyuMiao-1226/Demo1029/main/file.json
RAW_URL = st.text_input("GitHub Raw JSON URL", value="https://raw.githubusercontent.com/owner/repo/branch/path/to/file.json")

query = st.text_input("搜索关键词")
if st.button("搜索"):
    if not RAW_URL.strip():
        st.error("请填写 GitHub Raw JSON URL")
    else:
        with st.spinner("正在从 GitHub 读取 JSON..."):
            try:
                r = requests.get(RAW_URL, timeout=15)
                r.raise_for_status()
                data = r.json()  # 假设 JSON 是 list 或 dict
            except requests.exceptions.JSONDecodeError:
                st.error("该链接内容不是有效的 JSON。")
                st.stop()
            except requests.RequestException as e:
                st.error(f"请求失败：{e}")
                st.stop()

        # 简单搜索：在字符串化后的项中查找关键词（大小写不敏感）
        def matches(item, q):
            return q.lower() in str(item).lower()

        if isinstance(data, list):
            results = [item for item in data if (query and matches(item, query))] if query else data
        elif isinstance(data, dict):
            # 对 dict：如果有查询，在键或值字符串中查
            if query:
                results = {k: v for k, v in data.items() if matches({k: v}, query)}
            else:
                results = data
        else:
            st.warning("JSON 不是 list 或 dict，原样显示。")
            results = data

        st.subheader("结果")
        st.json(results)
        st.caption("提示：若需要检索整个仓库的多个 JSON 文件，可维护一个包含多个 raw 链接的列表并循环请求。")
