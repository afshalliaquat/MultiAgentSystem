from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain
from langchain_core.messages import ToolMessage, AIMessage


def extract_urls_from_messages(messages: list) -> list[str]:
    """Pull URLs out of ToolMessage results in the agent message history."""
    urls = []
    for msg in messages:
        if isinstance(msg, ToolMessage):
            # Tool results contain the raw search results with URLs
            content = msg.content
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("url"):
                        urls.append(block["url"])
            elif isinstance(content, str):
                # Sometimes URLs are embedded as plain text — extract them
                import re
                found = re.findall(r'https?://[^\s\'"<>]+', content)
                urls.extend(found)
    return list(dict.fromkeys(urls))  # deduplicate, preserve order


def content_to_string(content) -> str:
    """Safely convert agent message content to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))
                elif block.get("type") == "reference":
                    pass  # skip citation markers
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)


def research_pipeline(topic: str) -> dict:

    state = {}

    # ── Step 1: Search Agent ──────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 1: Search Agent is Working")
    print("=" * 50)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user", f"Find recent and reliable information on: {topic}")]
    })

    all_messages = search_results["messages"]

    # Convert the final answer to a clean string
    state["search_results"] = content_to_string(all_messages[-1].content)

    # Extract URLs from intermediate tool messages
    state["urls"] = extract_urls_from_messages(all_messages)

    print("\nSearch Summary:\n", state["search_results"])
    print("\nExtracted URLs:", state["urls"])

    # ── Step 2: Reader Agent ──────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 2: Reader Agent is Working")
    print("=" * 50)

    # Give the reader the URLs directly — not the raw content blob
    urls_text = "\n".join(state["urls"][:3])  # top 3 URLs

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Scrape the most relevant of these URLs about '{topic}' "
            f"and extract key information:\n\n{urls_text}"
        )]
    })

    state["scraped_content"] = content_to_string(reader_results["messages"][-1].content)
    print("\nScraped Content:\n", state["scraped_content"])

    # ── Step 3: Writer Chain ──────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 3: Writer Chain is Working")
    print("=" * 50)

    research_combined = (
        f"Search Results:\n{state['search_results']}\n\n"
        f"Scraped Content:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nReport:\n", state["report"])

    # ── Step 4: Critic Chain ──────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("Step 4: Critic Chain is Reviewing")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    print("\nFeedback:\n", state["feedback"])

    print(type(state["report"]))
    print(state["report"][:200])

    return state


if __name__ == "__main__":
    topic = input("Enter a research topic: ")
    research_pipeline(topic)