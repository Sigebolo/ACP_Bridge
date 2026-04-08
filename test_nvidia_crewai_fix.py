from crewai import Agent, Task, Crew, LLM
import os

def test_crewai_nvidia_fix():
    # Set up the LLM with the verified working model
    nvidia_llm = LLM(
        model="nvidia_nim/meta/llama-3.1-8b-instruct",
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1",
        temperature=0.7
    )
    
    # Create a simple agent
    test_agent = Agent(
        role="Tester",
        goal="Verify API connectivity",
        backstory="A simple testing agent",
        llm=nvidia_llm,
        verbose=True
    )
    
    # Create a simple task
    test_task = Task(
        description="Say 'The connection is successful' if you can read this.",
        expected_output="A confirmation message",
        agent=test_agent
    )
    
    # Create the crew
    test_crew = Crew(
        agents=[test_agent],
        tasks=[test_task],
        verbose=True
    )
    
    # Execute
    try:
        result = test_crew.kickoff()
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_crewai_nvidia_fix()
