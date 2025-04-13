def stream_error(text: str):
    async def text_stream():
        yield text
    return text_stream()