from openai import OpenAI

def test_nvidia_direct():
    client = OpenAI(
      base_url = "https://integrate.api.nvidia.com/v1",
      api_key = "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"
    )
    
    print("Connecting to NVIDIA NIM with nemotron-3-super-120b-a12b...")
    
    try:
        completion = client.chat.completions.create(
          model="nvidia/nemotron-3-super-120b-a12b",
          messages=[{"role":"user","content":"Hello, please introduce yourself briefly."}],
          temperature=1,
          top_p=0.95,
          max_tokens=1024,
          extra_body={"chat_template_kwargs":{"enable_thinking":True},"reasoning_budget":1024},
          stream=True
        )
        
        print("\n--- Response ---\n")
        for chunk in completion:
          if not chunk.choices:
            continue
          reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
          if reasoning:
            print(reasoning, end="", flush=True)
          if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)
        print("\n\n--- End of Response ---")
    except Exception as e:
        print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    test_nvidia_direct()
