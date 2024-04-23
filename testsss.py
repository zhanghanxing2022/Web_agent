from gradio_client import Client

client = Client("https://modelscope.cn/api/v1/studio/qwen/Qwen1.5-110B-Chat-demo/gradio/")
result = client.predict(
		"Hello!!",	# str  in 'Input' Textbox component
		[["Hello!",null]],	# Tuple[str | Dict(file: filepath, alt_text: str | None) | None, str | Dict(file: filepath, alt_text: str | None) | None]  in 'Qwen1.5-110B-Chat' Chatbot component
		"Hello!!",	# str  in 'parameter_8' Textbox component
		api_name="/model_chat"
)
print(result)