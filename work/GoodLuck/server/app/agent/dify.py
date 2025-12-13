import requests


def dify(user_input, conversation_id=None, user_id="default_user"):
    """
    与 Dify 应用进行对话，并维持上下文

    :param user_input: 用户输入的文本
    :param conversation_id: 会话 ID，首次对话可为空
    :param user_id: 用户标识，用于区分不同用户
    :return: Dify API 的响应，包含回答和新的 conversation_id
    """
    url = "https://api.dify.ai/v1/chat-messages"

    headers = {
        "Authorization": "Bearer app-zjP4yq8LTDyJIBsaoCR6unW2",  # 替换为你的实际 API 密钥
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},  # 这里可以传入你在 Dify 应用中定义的输入变量
        "query": user_input,
        "response_mode": "streaming",  # 推荐使用流式模式，体验更好
        "user": user_id,
        "conversation_id": conversation_id  # 首次对话不传或传空字符串，后续对话传入上次返回的 ID
    }

    response = requests.post(url, json=payload, headers=headers, stream=True)

    return response


